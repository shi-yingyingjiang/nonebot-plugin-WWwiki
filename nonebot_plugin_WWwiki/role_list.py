import json
from io import BytesIO

import httpx
from nonebot import on_command
from PIL import Image, ImageDraw, ImageFont

from .util import UniMessage

url = 'https://api.kurobbs.com/wiki/core/catalogue/item/getPage'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Wiki_type': '9'

}
listdata = {
    'catalogueId': '1105',
    'page': '1',
    'limit': '1000'
}
role_list = on_command("鸣潮角色列表")


@role_list.handle()
async def rolelistimg():
    async with httpx.AsyncClient() as client:
        role_list_r = await client.post(url, headers=headers, data=listdata)
        data = json.loads(role_list_r.text)
        records = data.get('data').get('results').get('records')
        matching_name = [item['name'] for item in records]
        # print(matching_entryIds)

        # 设置图片参数
        image_width = 800
        image_height = 50 * len(matching_name) + 50  # 为标题预留空间
        title = "角色列表"
        font_path = 'STKAITI.TTF'
        font_size_title = 40  # 标题的字体大小
        font_size_names = 30
        line_spacing = 20
        text_color = 'black'
        bg_color = 'white'

        # 创建图片
        img = Image.new('RGB', (image_width, image_height), bg_color)
        draw = ImageDraw.Draw(img)

        # 绘制标题
        title_bbox = draw.textbbox((0, 0), title, font=ImageFont.truetype(font_path, font_size_title))
        title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
        title_x = (image_width - title_width) // 2
        title_y = 20  # 留出一定的顶部边距
        draw.text((title_x, title_y), title, fill=text_color, font=ImageFont.truetype(font_path, font_size_title))

        # 绘制名字
        y_offset = title_y + title_height + 10  # 标题下方留空隙
        for name in matching_name:
            bbox = draw.textbbox((0, 0), name, font=ImageFont.truetype(font_path, font_size_names))
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = (image_width - text_width) // 2
            y = y_offset + (text_height + line_spacing) // 2
            draw.text((x, y), name, fill=text_color, font=ImageFont.truetype(font_path, font_size_names))
            y_offset += text_height + line_spacing
        img_byte = BytesIO()
        img.save(img_byte, format='PNG')
        # img_byte.seek(0)

        await UniMessage.image(raw=img_byte).finish()
