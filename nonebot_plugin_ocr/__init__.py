import nonebot
from nonebot import logger

from .config import PluginConfig, from_toml
from .ocr import init_ocr, get_ocr_callers
from .bot import init_bot, get_matchers


global_config = nonebot.get_driver().config
default_path = '.ocr/config.toml'
plugin_config = from_toml(global_config.ocr_config_path if hasattr(global_config, 'ocr_config_path') else default_path)


try:
    init_ocr(plugin_config.ocr)
    init_bot(plugin_config.bot, get_ocr_callers())
    logger.info('Successfully initialized plugin')
except Exception as e:
    logger.error(type(e))
    logger.error(e)
    logger.error('Failed to initialize plugin')
