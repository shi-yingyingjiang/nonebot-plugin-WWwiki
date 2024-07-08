from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import on_command


help_img = on_command('鸣潮wiki帮助')


@help_img.handle()
async def img():
    img_path = 'help.png'
    await help_img.finish(MessageSegment.image(img_path))