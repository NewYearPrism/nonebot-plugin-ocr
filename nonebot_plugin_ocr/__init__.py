import nonebot

from nonebot import logger
from nonebot.plugin import PluginMetadata

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


__plugin_meta__ = PluginMetadata(
    name='文字识别',
    description='识别图片中的文字',
    usage=f'''文字识别命令：{"，".join(plugin_config.bot.ocr_commands)}
    命令格式：<命令> [其他参数]
    使用方法：
    1，发送命令并附带图片
    2，使用命令回复带有图片的消息
    更多信息请访问插件主页 https://github.com/NewYearPrism/nonebot-plugin-ocr''',
    config=config.PluginConfig,
)
