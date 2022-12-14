from typing import Callable, Awaitable

from nonebot import logger
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.typing import T_State

from ..config import OnebotConfig
from ..ocr.client import Result as OcrResult, Error as OcrError


class Onebot11Bot:
    def __init__(self, config, call_ocr, make_data, make_param):
        self.config: OnebotConfig = config
        self.call_ocr: Callable[[dict, dict], Awaitable[OcrResult | OcrError]] = call_ocr
        self.make_data: Callable[[str], dict] = make_data
        self.make_param: Callable[[str], dict] = make_param

    # async def ocr_rule_checker(self) -> bool:
    #     return True

    async def permission_checker(self, event: MessageEvent) -> bool:
        if isinstance(event, GroupMessageEvent):
            return str(event.user_id) in self.config.whitelist_user \
                   or str(event.group_id) in self.config.whitelist_group
        elif isinstance(event, PrivateMessageEvent):
            return str(event.user_id) in self.config.whitelist_user
        else:
            return False

    async def ocr_handle_command(self, matcher: Matcher, event: MessageEvent, state: T_State):
        img = None
        if event.message.count('image'):
            img = event.message.get('image', 1)
            logger.debug(f'Got image in message {event.message}')
        elif event.reply and event.reply.message.count('image'):
            img = event.reply.message.get('image', 1)
            logger.debug(f'Got image in reply message {event.reply.message}')
        if img:
            matcher.set_arg('img', img)
        state['ocr_param'] = self.make_param(event.message.extract_plain_text())

    async def ocr_got_img(self, bot: Bot, matcher: Matcher, state: T_State, img_candidate: Message = Arg('img')):
        if img_candidate.count('image'):
            if 'url' in img_candidate.get('image')[0].data:
                img = img_candidate.get('image')[0].data.get('url')
            else:
                img_file = img_candidate.get('image')[0].data.get('file')
                img = (await bot.get_image(file=img_file)).get('url')
            data = self.make_data(img)
            param = state.get('ocr_param')
            reply: Message = Message()
            try:
                r = await self.call_ocr(data, **param)
                match r:
                    case OcrResult() as result:
                        reply = Message([MessageSegment.text(s) for s in result.get_words()])
                    case OcrError() as error:
                        reply = Message([MessageSegment
                                        .text(f'OCR?????????{str(type(error))}\n???????????????{error.get_error_message()}')])
                    case _:
                        reply = Message([MessageSegment.text('????????????')])
                        raise RuntimeError('OCR caller returned a unkown object')
            except Exception as e:
                logger.error(e)
            finally:
                await matcher.finish(reply)
        else:
            await matcher.finish('?????????')
