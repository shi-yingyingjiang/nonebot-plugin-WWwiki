# coding=utf-8
from pathlib import Path

from nonebot import on_command

from .util import UniMessage

help_img = on_command('鸣潮wiki帮助')


@help_img.handle()
async def img():
    await UniMessage.image(path=Path(__file__).parent.joinpath("help.png")).finish()
