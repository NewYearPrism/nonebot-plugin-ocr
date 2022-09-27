import os

import tomli
from nonebot import logger
from pydantic import BaseModel, validator


class OnebotConfig(BaseModel, extra='ignore'):
    whitelist_group: set[str] = set()
    whitelist_user: set[str] = set()


class BotConfig(BaseModel):
    ocr_commands: set[str] = {'ocr'}
    onebot: OnebotConfig = OnebotConfig()


class BaiduCloudConfig(BaseModel, extra='ignore'):
    api_key: str = ''
    secret_key: str = ''
    default_api: str = 'general_basic'
    default_language: str = 'CHN_ENG'
    caching: str = 'all'
    cache_expire_time: int = 7 * 24 * 60 * 60

    @validator('cache_expire_time', allow_reuse=True)
    def time_must_greater_than_zero(cls, v):
        if v <= 0:
            raise ValueError('cache expire time must greater than zero')
        return v


class OcrConfig(BaseModel, extra='ignore'):
    backend: str = ''
    baidu_cloud: BaiduCloudConfig = BaiduCloudConfig()


class PluginConfig(BaseModel, extra='ignore'):
    bot: BotConfig = BotConfig()
    ocr: OcrConfig = OcrConfig()


def from_toml(config_path: str) -> PluginConfig:
    conf = ''
    try:
        with open(config_path) as f:
            conf = f.read()
    except IOError as e:
        logger.error(e)
        logger.error(f'Failed to read configuration file: {os.path.abspath(config_path)}')
    conf_data = {}
    try:
        conf_data = tomli.loads(conf)
    except tomli.TOMLDecodeError as e:
        logger.error(e)
        logger.error(f'Failed to parse configuration: {os.path.abspath(config_path)}')
    return PluginConfig.parse_obj(conf_data)
