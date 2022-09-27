import json

import httpx
import diskcache

from nonebot_plugin_ocr.ocr.client import Client as OcrClient, Result as OcrResult, Error as OcrError
from nonebot_plugin_ocr.config import BaiduCloudConfig


class BaiduCloudBaseResult(OcrResult):
    log_id: int
    words_result: list[dict]
    words_result_num: int

    def get_words(self) -> list[str]:
        return [d.get('words') for d in self.words_result]


class BaiduCloudError(OcrError):
    error_code: int
    error_msg: str

    def get_error_message(self) -> str:
        return f'[{self.error_code}] {self.error_msg}'


class BaiduCloudClient(OcrClient):
    API = {'general_basic', 'general', 'accurate_basic', 'accurate'}
    LANGUAGE_GENERAL = {'CHN_ENG', 'ENG', 'JAP', 'KOR', 'FRE', 'SPA', 'POR', 'GER', 'ITA', 'RUS'}
    LANGUAGE_ACCURATE = LANGUAGE_GENERAL | {'DAN', 'DUT', 'MAL', 'SWE', 'IND', 'POL', 'ROM', 'TUR', 'GRE', 'HUN'}
    TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
    OCR_URL_PREFIX = 'https://aip.baidubce.com/rest/2.0/ocr/v1/'
    LANGUAGE_ALIAS = {
        'ch': 'CHN_ENG',
        'chn': 'CHN_ENG',
        'zh': 'CHN_ENG',
        'cn': 'CHN_ENG',
        'en': 'ENG',
        'jp': 'JAP',
    }
    API_ALIAS = {
        'g': 'general_basic',
        'gl': 'general',
        'a': 'accurate_basic',
        'al': 'accurate',
    }

    @staticmethod
    def parse_content(content: str) -> BaiduCloudBaseResult | BaiduCloudError:
        match json.loads(content):
            case {'log_id': _} as d:
                return BaiduCloudBaseResult.parse_obj(d)
            case {'error_code': _} as d:
                return BaiduCloudBaseResult.parse_obj(d)
            case _:
                raise ValueError('Failed to parse content')

    _cache = diskcache.Cache(directory='.ocr/cache/baidu_cloud', disk=diskcache.JSONDisk, disk_compress_level=0)

    @classmethod
    def generate_client(cls, config: BaiduCloudConfig) -> 'BaiduCloudClient':
        if config.api_key and config.secret_key:
            r = httpx.get(cls.TOKEN_URL, params={'grant_type': 'client_credentials',
                                                 'client_id': config.api_key,
                                                 'client_secret': config.secret_key})
            access_token = json.loads(r.text).get('access_token')
            if not access_token:
                raise RuntimeError('Failed to validate Baidu Cloud keys')
            else:
                return cls(config.api_key,
                           config.secret_key,
                           default_api=config.default_api,
                           default_language=config.default_language,
                           caching=config.caching,
                           cache_expire=config.cache_expire_time)
        else:
            raise ValueError('Baidu Cloud keys is empty')

    @classmethod
    async def request_token(cls, api_key: str, secret_key: str) -> str:
        params = {'grant_type': 'client_credentials', 'client_id': api_key, 'client_secret': secret_key}
        async with httpx.AsyncClient() as c:
            r = await c.get(cls.TOKEN_URL, params=params)
            return r.text

    @classmethod
    async def request_ocr(cls, api: str, access_token: str, __data: dict[str, str], **param) -> str:
        request_url = cls.OCR_URL_PREFIX + api
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {'access_token': access_token}
        data.update(__data | param)
        async with httpx.AsyncClient() as c:
            r = await c.post(request_url, data=data, headers=headers)
            return r.text

    def __init__(self, api_key: str, secret_key: str, **extra):
        self._api_key: str = api_key
        self._secret_key: str = secret_key
        self._default_api: str = ({extra.get('default_language')} & self.API or {'general_basic'}).pop()
        self._default_language: str = ({extra.get('default_language')} & self.LANGUAGE_GENERAL or {'CHN_ENG'}).pop()
        self._caching: str = extra.get('caching') or 'all'
        self._cache_expire: int = extra.get('cache_expire') \
            if isinstance(extra.get('cache_expire'), int) and extra.get('cache_expire') > 0 \
            else 7 * 24 * 60 * 60

    async def ocr_by_httpurl(self, httpurl: str, **param) -> str:
        data = {'url': httpurl}
        return await self._ocr(data, **param)

    async def ocr_by_base64image(self, b64image: str, **param) -> str:
        data = {'image': b64image}
        return await self._ocr(data, **param)

    async def _get_access_token(self) -> str:
        if self._caching == 'all' or self._caching == 'token':
            cached = self._cache.get(json.dumps({'api_key': self._api_key, 'secret_key': self._secret_key}))
            if cached:
                return cached
        access_token = json.loads(await self.request_token(self._api_key, self._secret_key)).get('access_token')
        if not access_token:
            raise RuntimeError('Failed to acquire Baidu Cloud access token')
        if self._caching == 'all' or self._caching == 'token':
            self._cache.set(json.dumps({'api_key': self._api_key, 'secret_key': self._secret_key}), access_token,
                            tag='token', expire=30*24*60*60)  # access token 有效期为30天
        return access_token

    async def _ocr(self, data: dict[str, str], **param) -> str:
        if self._caching == 'all':
            cached = self._cache.get(json.dumps(data | param))
            if cached:
                return cached
        access_token = await self._get_access_token()
        if not access_token:
            raise RuntimeError('Baidu Cloud access token missing')
        api: str = param.get('api')
        lang: str = param.get('lang')
        match api:
            case api if api in self.API:
                pass
            case api if api in self.API_ALIAS:
                api = self.API_ALIAS.get(api)
            case _:
                api = self._default_api
        langs = self.LANGUAGE_GENERAL if api.startswith('general') else self.LANGUAGE_ACCURATE
        match lang:
            case lang if lang and lang.upper() in langs:
                lang = lang.upper()
            case lang if lang and lang.lower() in self.LANGUAGE_ALIAS:
                lang = self.LANGUAGE_ALIAS.get(lang.lower())
            case _:
                lang = self._default_language
        ret_text = await self.request_ocr(api, access_token, data, lang=lang)
        if self._caching == 'all':
            self._cache.set(json.dumps(data | param), ret_text, tag='ocr', expire=self._cache_expire)
        return ret_text
