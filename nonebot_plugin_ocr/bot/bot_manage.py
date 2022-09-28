from typing import Type, Callable, Awaitable

from nonebot import on_startswith
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER

from ..config import BotConfig
from .onebot11 import Onebot11Bot
from .tool import parse_arg, parse_link

matchers: dict[str, Type[Matcher]] = dict()
bots: dict[str, ...] = dict()
ocr_callers: list[Callable[[...], Awaitable]] = []


def init_bot(bot_config: BotConfig, ocr_: list[Callable[[...], Awaitable]]):
    ocr_callers.extend(ocr_)
    matchers.update(ocr=on_startswith(msg=tuple(bot_config.ocr_commands), permission=SUPERUSER))
    bots.update(onebot11=Onebot11Bot(bot_config.onebot, ocr_callers[-1], parse_link, parse_arg))
    ocr = matchers.get('ocr')
    o11 = bots.get('onebot11')
    ocr.permission = ocr.permission | o11.permission_checker
    ocr.handle()(o11.ocr_handle_command)
    ocr.got('img', '请发送图片')(o11.ocr_got_img)


def get_matchers():
    return matchers