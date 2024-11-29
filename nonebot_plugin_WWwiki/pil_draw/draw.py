# coding=utf-8
from PIL import Image
from nonebot import logger, require

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic

from .tools import save_image


async def draw_main(draw_data: dict, template_name: None):
    logger.debug(f"template_name: {template_name}")
    logger.debug(f"draw_data: {draw_data}")
    image = Image.new("RGBA", (100, 100), (50, 50, 50, 255))

    return save_image(image, to_bytes=True)


async def draw_name():
    return
