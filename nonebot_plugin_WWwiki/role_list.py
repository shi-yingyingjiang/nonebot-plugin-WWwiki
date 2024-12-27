# coding=utf-8
import json
from io import BytesIO
import httpx
from nonebot import on_command
from PIL import Image, ImageDraw, ImageFont
from .util import UniMessage, font_path

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
        records = data['data']['results']['records']
        processed_titles = []

        for item in records:
            content = item["content"]
            title = content["title"]
            show_teaser_icon_num = content.get("showTeaserIconNum")

            # 根据 showTeaserIconNum 添加角标
            if show_teaser_icon_num == 2:
                title += " (预)"
            elif show_teaser_icon_num == 1:
                title += " (新)"

            processed_titles.append(title)

        # 输出处理后的标题

        from PIL import Image, ImageDraw, ImageFont

        # 定义一些常量
        FONT_PATH =  font_path /'STXingkai.TTF'
        FONT_SIZE = 20
        LINE_SPACING = 5
        MAX_COLUMNS = 2  # 改为两列 
        COLUMN_SPACING = 10  # 列之间的间距
        BORDER = 50  # 上下左右边界距离

        # 加载字体
        try:
            font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
            superscript_font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE // 2)  # 角标字体大小减半
        except IOError:
            print("Error loading font. Using default font.")
            font = ImageFont.load_default()
            superscript_font = ImageFont.load_default()

        # 计算每个名字的宽度
        name_widths = [ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(name, font=font) for name in processed_titles]

        # 计算每个角标的宽度
        superscripts = ['(新)' if '(新)' in name else '(预)' if '(预)' in name else '' for name in processed_titles]
        superscript_widths = [ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(superscript, font=superscript_font) for superscript in superscripts]

        # 计算每列的名字
        columns = [processed_titles[i::MAX_COLUMNS] for i in range(MAX_COLUMNS)]

        # 计算每列中最长名字的宽度
        column_widths = [max([name_widths[i] + superscript_widths[i] for i, name in enumerate(processed_titles) if i % MAX_COLUMNS == j], default=0) for j in range(MAX_COLUMNS)]

        # 计算每列的总高度
        column_heights = [len(column) * (FONT_SIZE + LINE_SPACING) for column in columns]

        # 动态计算图片的宽度和高度
        IMAGE_WIDTH = int(sum(column_widths) + (MAX_COLUMNS - 1) * COLUMN_SPACING + 2 * BORDER)
        IMAGE_HEIGHT = int(max(column_heights) + 2 * BORDER)

        # 创建一个空白图片
        image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
        draw = ImageDraw.Draw(image)

        # 计算每列的起始位置
        x_texts = [int(sum(column_widths[:i]) + i * COLUMN_SPACING + BORDER) for i in range(MAX_COLUMNS)]

        # 计算每列的垂直居中位置
        vertical_offsets = [(IMAGE_HEIGHT - height - 2 * BORDER) / 2 for height in column_heights]

        # 绘制文本
        for i, name in enumerate(processed_titles):
            col_index = i % MAX_COLUMNS
            row_index = i // MAX_COLUMNS
            
            # 计算当前名字的宽度，并根据最长名字的宽度对齐
            name_width = name_widths[i]
            x_text = x_texts[col_index] + (column_widths[col_index] - name_width) / 2
            
            # 计算垂直居中位置
            y_text = vertical_offsets[col_index] + row_index * (FONT_SIZE + LINE_SPACING) + BORDER
            
            # 绘制名字
            base_name = name.split('(')[0].strip()
            draw.text((x_text, y_text), base_name, fill='black', font=font)
            
            # 绘制角标
            superscript = superscripts[i]
            if superscript:
                superscript_x = x_text + name_width + 1  # 右侧偏移
                superscript_y = y_text - 4  # 向上偏移
                draw.text((superscript_x, superscript_y), superscript, fill='red', font=superscript_font)
        img_byte = BytesIO()
        image.save(img_byte, format='PNG')


        await UniMessage.image(raw=img_byte).finish()
