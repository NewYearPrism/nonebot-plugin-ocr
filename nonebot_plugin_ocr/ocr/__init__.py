import functools

from nonebot import logger

from ..config import OcrConfig
from .client import Client, Result as OcrResult, Error as OcrError
from .baidu_cloud import BaiduCloudClient

ocr_clients: dict[str, Client] = dict()


async def ocr(data: dict[str, str], *, ocr_client: Client, **param) -> OcrResult | OcrError:
    match data:
        case {'httpurl': url}:
            return ocr_client.parse_content(await ocr_client.ocr_by_httpurl(url, **param))
        case {'base64image': image}:
            return ocr_client.parse_content(await ocr_client.ocr_by_base64image(image, **param))
        case _:
            raise ValueError(f'Data not supported: {data}')


def init_ocr(ocr_config: OcrConfig):
    match ocr_config.backend:
        case 'baidu_cloud' as backend:
            try:
                baidu_client = BaiduCloudClient.generate_client(ocr_config.baidu_cloud)
                ocr_clients.update(baidu_cloud=baidu_client)
                logger.info(f'Successfully created OCR application: {backend}')
            except Exception:
                logger.error(f'Failed to create OCR application: {backend}')
                raise


def get_ocr_callers():
    return [functools.partial(ocr, ocr_client=c) for c in ocr_clients.values()]
