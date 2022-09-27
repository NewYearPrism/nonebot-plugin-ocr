from typing import Callable, Awaitable

from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.typing import T_State

from nonebot_plugin_ocr.config import OnebotConfig
from nonebot_plugin_ocr.ocr.client import Result


class Onebot11Bot:
    def __init__(self, config, call_ocr, make_data, make_param):
        self.config: OnebotConfig = config
        self.call_ocr: Callable[[dict, dict], Awaitable[Result]] = call_ocr
        self.make_data: Callable[[str], dict] = make_data
        self.make_param: Callable[[str], dict] = make_param

    # async def ocr_rule_checker(self) -> bool:
    #     return True

    async def permission_checker(self, event: MessageEvent) -> bool:
        if isinstance(event, GroupMessageEvent):
            return event.user_id in self.config.whitelist_user or event.group_id in self.config.whitelist_group
        elif isinstance(event, PrivateMessageEvent):
            return event.user_id in self.config.whitelist_user
        else:
            return False

    async def ocr_handle_command(self, matcher: Matcher, event: MessageEvent, state: T_State):
        img = None
        if event.message.count('image'):
            img = event.message.get('image', 1)
        elif event.reply and event.reply.message.count('image'):
            img = event.reply.message.get('image', 1)
        if img:
            matcher.set_arg('img', img)
        state['ocr_param'] = self.make_param(event.message.extract_plain_text())

    async def ocr_got_img(self, matcher: Matcher, state: T_State, img_candidate: Message = Arg('img')):
        if img_candidate.count('image'):
            img = img_candidate.get('image')[0].data.get('file')
            data = self.make_data(img)
            param = state.get('ocr_param')
            result = await self.call_ocr(data, **param)
            reply = Message([MessageSegment.text(s) for s in result.get_words()])
            await matcher.finish(reply)
        else:
            await matcher.finish('没有识别到图片')
