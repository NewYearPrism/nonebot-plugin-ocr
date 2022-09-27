import re

from nonebot import logger

spliter = re.compile(r'\s+')


def parse_arg(cmd: str) -> dict[str, str]:
    args = re.split(spliter, cmd)
    param = dict()
    if len(args) >= 2:
        param['lang'] = args[1]
    if len(args) >= 3:
        param['api'] = args[2]
    return param


def parse_link(link: str) -> dict[str, str]:
    if link.startswith('http'):
        return {'httpurl': link}
    elif link.startswith('base64'):
        return {'base64image': link.removeprefix('base64://')}
    else:
        raise ValueError(f'Link not support: {link}')
