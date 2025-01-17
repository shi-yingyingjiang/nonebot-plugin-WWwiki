# coding=utf-8
from PIL import Image
from nonebot import logger, require
from .config import draw_color
from .tools import save_image, load_image, draw_text, image_resize2, circle_corner, draw_form, parser_html, mix_image, \
    get_html_text_url
from bs4 import BeautifulSoup

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic

# 推荐安装JiYingHuiPianHuiSong-2.ttf字体
font_file_path = "JiYingHuiPianHuiSong-2.ttf"


async def draw_main(draw_data: dict, temp_name: str = None, temp_path: str = None):
    logger.debug(f"draw_data: {draw_data}")
    template_name = temp_path.split("/")[-1]
    logger.debug(f"template_path: {temp_path}")
    logger.debug(f"template_name: {template_name}")

    # 鸣潮角色查询
    if template_name == "rolecard":
        return await draw_rolecard(draw_data)
    # 鸣潮技能查询
    elif template_name == "echolink":
        return await draw_echolink(draw_data)
    # 鸣潮共鸣链查询
    elif template_name == "recommendation":
        return await draw_recommendation(draw_data)
    # 鸣潮
    elif template_name == "":
        return await draw_name(draw_data)
    # 鸣潮
    elif template_name == "":
        return await draw_name(draw_data)
    # 鸣潮
    elif template_name == "":
        return await draw_name(draw_data)
    # 鸣潮
    elif template_name == "":
        return await draw_name(draw_data)

    img = await template_to_pic(
        temp_path,
        temp_name,
        draw_data,
    )
    return img


async def draw_rolecard(draw_data: dict):
    """
    绘制
    """
    forms_data_info = [
        [
            {"color": draw_color("群组名称"), "size": 28, "text": draw_data.get("attribute").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("attribute").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": "特殊料理"},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("specialcuisine")},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": draw_data.get("gender").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("gender").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": "中文cv"},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("zhcv")},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": draw_data.get("birthplace").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("birthplace").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": "日文cv"},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("jpcv")},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": draw_data.get("weapon").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("weapon").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": "英文cv"},
            {"color": draw_color("群组内容"), "size": 22, "text": draw_data.get("encv")},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": "身份"},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("identity")},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": "韩文cv"},
            {"color": draw_color("群组内容"), "size": 22, "text": draw_data.get("kocv")},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": "所属"},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("affiliation")},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": "实装版本"},
            {"color": draw_color("群组内容"), "size": 26, "text": draw_data.get("version")},
        ],
    ]
    combat_data = draw_data.get("combat_data")
    forms_data_combat = [
        [
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[0][0]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[2][0]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[3][0]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[4][0]},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[0][1]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[2][1]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[3][1]},
            {"color": draw_color("群组内容"), "size": 24, "text": combat_data[4][1]},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[0][2]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[2][2]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[3][2]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[4][2]},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[0][3]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[2][3]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[3][3]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[4][3]},
        ], [
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[0][4]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[2][4]},
            {},
            {"color": draw_color("群组名称"), "size": 28, "text": combat_data[3][4]},
            {"color": draw_color("群组内容"), "size": 26, "text": combat_data[4][4]},
        ],
    ]
    image_x, image_y = (900, 0)
    image_y += 643  # 基础信息界面

    paste_image = await draw_form(
        forms_data_info,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]

    # 战斗风格-标题
    image_y += 15
    image_y += 40

    # 战斗风格
    image_y += 15
    image_y += 105

    # 战斗数据-标题
    image_y += 15
    image_y += 40

    # 战斗数据
    image_y += 15
    paste_image = await draw_form(
        forms_data_combat,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]

    image_y += 50  # 底部留空

    # ## 开始绘制 ##
    image = Image.new("RGBA", (image_x, image_y), draw_color("背景"))

    # 立绘
    paste_image = await load_image(draw_data.get("roleimg"))
    paste_image = image_resize2(paste_image, (720, 720))
    image.alpha_composite(paste_image, (263, -57))

    # 角色logo
    paste_image = await load_image(draw_data.get("campIcon"))
    paste_image = image_resize2(paste_image, (128, 128))
    paste_color = Image.new("RGBA", (128, 128), "#FFFFFFFF")
    image.paste(paste_color, (745, 22), paste_image)

    # 图标
    paste_image = await draw_text(
        "鸣潮WIKI",
        size=36,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("图标"),
        calculate=False
    )
    image.alpha_composite(paste_image, (25, 26))

    # 副图标
    paste_image = await draw_text(
        "wuthering waves",
        size=19,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("副图标"),
        calculate=False
    )
    image.alpha_composite(paste_image, (17, 60))

    # 标题-名称
    paste_image = await draw_text(
        draw_data.get("title"),
        size=72,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 150))

    # 副标题-英文名称
    paste_image = await draw_text(
        draw_data.get("roleenname"),
        size=36,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("副标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 230))

    # 简介标题（共鸣能力）
    paste_image = await draw_text(
        draw_data.get("roleDescriptiontitle"),
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("简介标题"),
        calculate=False
    )
    paste_card = Image.new("RGBA", (paste_image.size[0] + 10, paste_image.size[1] + 10), draw_color("背景"))
    paste_card = circle_corner(paste_card, 10)
    image.alpha_composite(paste_card, (38 - 5, 346 - 5))
    image.alpha_composite(paste_image, (38, 346))

    # 简介内容（共鸣能力介绍）
    paste_image = await draw_text(
        draw_data.get("roleDescription"),
        size=24,
        textlen=16,
        fontfile=font_file_path,
        text_color=draw_color("简介内容"),
        calculate=False
    )
    paste_card = Image.new("RGBA", (paste_image.size[0] + 10, paste_image.size[1] + 10), draw_color("背景"))
    paste_card = circle_corner(paste_card, 10)
    image.alpha_composite(paste_card, (38 - 5, 383 - 5))
    image.alpha_composite(paste_image, (38, 383))

    x = 0
    y = 583

    # 基础消息-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "基础消息",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 基础消息
    y += 15
    paste_image = await draw_form(
        forms_data_info,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    # 战斗风格-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "战斗风格",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 战斗风格
    y += 15
    fighting_style = draw_data.get("fighting_style_content")
    fighting_style = parser_html(fighting_style)
    links = fighting_style.links
    texts = fighting_style.texts
    fighting_styles = []
    for i in range(len(links)):
        fighting_styles.append([links[i], texts[2 * i], texts[2 * i + 1]])
    # fighting_style = [["http://github.com/example.png", "text", "text"]]

    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, 105 + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), 105), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    paste_card = Image.new("RGBA", (850, 105), (0, 0, 0, 0))
    form_size = int(850 / len(fighting_styles))
    for i, fighting_style in enumerate(fighting_styles):
        paste_image = await load_image(fighting_style[0])
        paste_image = image_resize2(paste_image, (96, 96))
        paste_color = Image.new("RGBA", (96, 96), "#ffffff")
        paste_card.paste(paste_color, ((i * form_size), 5), paste_image)

        paste_image = await draw_text(
            fighting_style[1],
            size=30,
            textlen=10,
            fontfile=font_file_path,
            text_color=draw_color("群组内容"),
            calculate=False
        )
        paste_card.alpha_composite(paste_image, ((i * form_size) + 94, 15))

        if len(fighting_styles) == 1:
            textlen = 25
        elif len(fighting_styles) == 2:
            textlen = 15
        else:
            textlen = 9
        paste_image = await draw_text(
            fighting_style[2],
            size=20,
            textlen=textlen,
            fontfile=font_file_path,
            text_color=draw_color("群组名称"),
            calculate=False
        )
        paste_card.alpha_composite(paste_image, ((i * form_size) + 94, 52))

    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    y += paste_card.size[1]

    # 战斗数据-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "战斗数据",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 战斗数据
    y += 15
    paste_image = await draw_form(
        forms_data_combat,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    return save_image(image, to_bytes=True)


async def draw_echolink(draw_data: dict):
    """
    绘制
    """
    echolink_data = draw_data.get("content")

    echolink_data_combat = []
    links = parser_html(echolink_data).links

    soup = BeautifulSoup(echolink_data, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        if i == 0:
            continue
        i -= 1
        cols = row.find_all(['td', 'th'])
        cols_text = [col.get_text(strip=True) for col in cols]
        link = links[i]
        echolink_data_combat.append([
            {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
            {"color": "#ffffff", "type": "image", "size": (100, 100), "image": link},
            {"color": draw_color("群组内容"), "size": 25, "text": cols_text[1]},
            {},
        ])

    image_x, image_y = (900, 0)
    image_y += 643  # 基础信息界面

    paste_image = await draw_form(
        echolink_data_combat,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]

    image_y += 50  # 底部留空

    # ## 开始绘制 ##
    image = Image.new("RGBA", (image_x, image_y), draw_color("背景"))

    # 立绘
    paste_image = await load_image(draw_data.get("roleimg"))
    paste_image = image_resize2(paste_image, (720, 720))
    image.alpha_composite(paste_image, (263, -57))

    # 角色logo
    paste_image = await load_image(draw_data.get("campIcon"))
    paste_image = image_resize2(paste_image, (128, 128))
    paste_color = Image.new("RGBA", (128, 128), "#FFFFFFFF")
    image.paste(paste_color, (745, 22), paste_image)

    # 图标
    paste_image = await draw_text(
        "鸣潮WIKI",
        size=36,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("图标"),
        calculate=False
    )
    image.alpha_composite(paste_image, (25, 26))

    # 副图标
    paste_image = await draw_text(
        "wuthering waves",
        size=19,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("副图标"),
        calculate=False
    )
    image.alpha_composite(paste_image, (17, 60))

    # 标题-名称
    paste_image = await draw_text(
        draw_data.get("rolename"),
        size=72,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 150))

    # 副标题-英文名称
    paste_image = await draw_text(
        draw_data.get("roleenname"),
        size=36,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("副标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 230))

    # 简介标题（共鸣能力）
    paste_image = await draw_text(
        draw_data.get("roledescriptiontitle"),
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("简介标题"),
        calculate=False
    )
    paste_card = Image.new("RGBA", (paste_image.size[0] + 10, paste_image.size[1] + 10), draw_color("背景"))
    paste_card = circle_corner(paste_card, 10)
    image.alpha_composite(paste_card, (38 - 5, 346 - 5))
    image.alpha_composite(paste_image, (38, 346))

    # 简介内容（共鸣能力介绍）
    paste_image = await draw_text(
        draw_data.get("roledescription"),
        size=24,
        textlen=16,
        fontfile=font_file_path,
        text_color=draw_color("简介内容"),
        calculate=False
    )
    paste_card = Image.new("RGBA", (paste_image.size[0] + 10, paste_image.size[1] + 10), draw_color("背景"))
    paste_card = circle_corner(paste_card, 10)
    image.alpha_composite(paste_card, (38 - 5, 383 - 5))
    image.alpha_composite(paste_image, (38, 383))

    x = 0
    y = 583

    # 共鸣链-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "共鸣链",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 共鸣链
    y += 15
    paste_image = await draw_form(
        echolink_data_combat,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    return save_image(image, to_bytes=True)


async def draw_recommendation(draw_data: dict):
    """
    绘制
    """
    # 获取数据
    weapons_recommended = draw_data.get("weapons_recommended")
    echo_recommended = draw_data.get("echo_recommended")
    team_recommended = draw_data.get("team_recommended")
    skll_recommended = draw_data.get("skll_recommended")

    # 解析html - 武器推荐
    weapons_data = []
    links = parser_html(weapons_recommended).links
    soup = BeautifulSoup(weapons_recommended, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cols = row.find_all(['td', 'th'])
        cols_text = [col.get_text(strip=True) for col in cols]
        if cols_text[0].startswith("武器首位推荐"):
            cols_text[0] = "武器首位推荐\n" + cols_text[0][6:]

        right_cols_text_list = []
        right_cols = cols[1:]
        for num, col in enumerate(right_cols):
            paragraphs = col.find_all('p')
            for paragraph in paragraphs:
                right_cols_text_list.append(paragraph.get_text(strip=True))

        text = ""
        for t in right_cols_text_list:
            text += f"{t}\n \n"
        text = text.removesuffix("\n \n")
        cols_text[1] = text

        link1 = links[(i - 1) * 2]
        link2 = links[((i - 1) * 2) + 1]
        link2 = await load_image(link2)
        link2 = image_resize2(link2, (264, 86))
        link_image = await mix_image(link1, link2)
        if i == 0:
            weapons_data.append([
                {"color": draw_color("群组名称"), "size": 30, "text": cols_text[0]},
                {"color": draw_color("群组内容"), "size": 23, "text": cols_text[1]},
                {},
                {},
                {},
            ])
        else:
            weapons_data.append([
                {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
                {"color": None, "type": "image", "size": (150, 150), "image": link_image},
                {"color": draw_color("群组内容"), "size": 22, "text": cols_text[1]},
                {},
                {},
            ])

    # 解析html - 声骸推荐
    echo_data = []
    soup = BeautifulSoup(echo_recommended, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cols = row.find_all(['td', 'th'])
        cols_text = []
        text = get_html_text_url(cols[0].children)
        text = text.replace("\\xa0", "")
        cols_text.append(text)

        text = get_html_text_url(cols[1].children)
        text = text.replace("\\xa0", "")
        cols_text.append(text)

        echo_data.append([
            {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
            {"color": draw_color("群组内容"), "size": 22, "text": cols_text[1]},
            {},
            {},
            {},
        ])

    # 解析html - 配队推荐
    team_data = []
    links = parser_html(team_recommended).links
    soup = BeautifulSoup(team_recommended, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cols = row.find_all(['td', 'th'])
        cols_text = [col.get_text(strip=True) for col in cols]

        right_cols_text_list = []
        right_cols = cols[1:]
        for num, col in enumerate(right_cols):
            paragraphs = col.find_all('p')
            for paragraph in paragraphs:
                right_cols_text_list.append(paragraph.get_text(strip=True))

        text = ""
        for t in right_cols_text_list:
            text += f"{t}\n \n"
        text = text.removesuffix("\n \n")
        cols_text[1] = text

        cols_text[0] = cols_text[0].replace("\\xa0", "")
        cols_text[1] = cols_text[1].replace("\\xa0", "")

        if i in [0, 1] or cols_text[0] == "副输出":
            team_data.append([
                {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
                {"color": draw_color("群组内容"), "size": 22, "text": cols_text[1]},
                {},
                {},
                {},
            ])
        else:
            link = links[0]
            links.remove(link)
            team_data.append([
                {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
                {"color": None, "type": "image", "size": (130, 130), "image": link},
                {"color": draw_color("群组内容"), "size": 22, "text": cols_text[1]},
                {},
                {},
            ])

    # 解析html - 技能加点推荐
    skll_data = []
    links = parser_html(skll_recommended).links
    soup = BeautifulSoup(skll_recommended, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cols = row.find_all(['td', 'th'])
        cols_text = [col.get_text(strip=True) for col in cols]

        cols_text[1] = cols_text[1].replace("\\xa0", "")

        if i == 0:
            skll_data.append([
                {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
                {"color": draw_color("群组内容"), "size": 22, "text": cols_text[1]},
                {},
                {},
                {},
            ])
        else:
            link = links[0]
            links.remove(link)
            skll_data.append([
                {"color": draw_color("群组名称"), "size": 28, "text": cols_text[0]},
                {"color": "#ffffff", "type": "image", "size": (100, 100), "image": link},
                {"color": draw_color("群组内容"), "size": 22, "text": cols_text[1]},
                {},
                {},
            ])

    # 计算图片尺寸
    image_x, image_y = (900, 0)
    image_y += 643  # 基础信息界面

    # 武器推荐
    paste_image = await draw_form(
        weapons_data,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]
    image_y += 15

    # 声骸推荐
    image_y += 40
    image_y += 15
    paste_image = await draw_form(
        echo_data,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]
    image_y += 15

    # 配队推荐
    image_y += 40
    image_y += 15
    paste_image = await draw_form(
        team_data,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]
    image_y += 15

    # 技能加点推荐
    image_y += 40
    image_y += 15
    paste_image = await draw_form(
        skll_data,
        size_x=int(image_x * 0.95),
        calculate=True,
        font_file_path=font_file_path
    )
    image_y += paste_image.size[1]
    image_y += 15

    image_y += 35  # 底部留空

    # ## 开始绘制 ##
    image = Image.new("RGBA", (image_x, image_y), draw_color("背景"))

    # 卡片基础信息
    if True:
        # 立绘
        paste_image = await load_image(draw_data.get("roleimg"))
        paste_image = image_resize2(paste_image, (720, 720))
        image.alpha_composite(paste_image, (263, -57))

        # 角色logo
        paste_image = await load_image(draw_data.get("campIcon"))
        paste_image = image_resize2(paste_image, (128, 128))
        paste_color = Image.new("RGBA", (128, 128), "#FFFFFFFF")
        image.paste(paste_color, (745, 22), paste_image)

        # 图标
        paste_image = await draw_text(
            "鸣潮WIKI",
            size=36,
            textlen=99,
            fontfile=font_file_path,
            text_color=draw_color("图标"),
            calculate=False
        )
        image.alpha_composite(paste_image, (25, 26))

        # 副图标
        paste_image = await draw_text(
            "wuthering waves",
            size=19,
            textlen=99,
            fontfile=font_file_path,
            text_color=draw_color("副图标"),
            calculate=False
        )
        image.alpha_composite(paste_image, (17, 60))

        # 标题-名称
        paste_image = await draw_text(
            draw_data.get("rolename"),
            size=72,
            textlen=99,
            fontfile=font_file_path,
            text_color=draw_color("标题"),
            calculate=False
        )
        image.alpha_composite(paste_image, (38, 150))

        # 副标题-英文名称
        paste_image = await draw_text(
            draw_data.get("roleenname"),
            size=36,
            textlen=99,
            fontfile=font_file_path,
            text_color=draw_color("副标题"),
            calculate=False
        )
        image.alpha_composite(paste_image, (38, 230))

        # 简介标题（共鸣能力）
        paste_image = await draw_text(
            draw_data.get("roledescriptiontitle"),
            size=30,
            textlen=99,
            fontfile=font_file_path,
            text_color=draw_color("简介标题"),
            calculate=False
        )
        paste_card = Image.new("RGBA", (paste_image.size[0] + 10, paste_image.size[1] + 10), draw_color("背景"))
        paste_card = circle_corner(paste_card, 10)
        image.alpha_composite(paste_card, (38 - 5, 346 - 5))
        image.alpha_composite(paste_image, (38, 346))

        # 简介内容（共鸣能力介绍）
        paste_image = await draw_text(
            draw_data.get("roledescription"),
            size=24,
            textlen=16,
            fontfile=font_file_path,
            text_color=draw_color("简介内容"),
            calculate=False
        )
        paste_card = Image.new("RGBA", (paste_image.size[0] + 10, paste_image.size[1] + 10), draw_color("背景"))
        paste_card = circle_corner(paste_card, 10)
        image.alpha_composite(paste_card, (38 - 5, 383 - 5))
        image.alpha_composite(paste_image, (38, 383))

        x = 0
        y = 583

    # 武器推荐-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "武器推荐",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 武器推荐
    y += 15
    paste_image = await draw_form(
        weapons_data,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    # 声骸推荐-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "声骸推荐",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 声骸推荐
    y += 15
    paste_image = await draw_form(
        echo_data,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    # 配队推荐-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "配队推荐",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 配队推荐
    y += 15
    paste_image = await draw_form(
        team_data,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    # 技能加点推荐-标题
    y += 15
    paste_image = Image.new("RGBA", (10, 40), draw_color("卡片标题背景"))
    paste_image = circle_corner(paste_image, 5)
    image.alpha_composite(paste_image, (x + 20, y))
    paste_image = await draw_text(
        "技能加点推荐",
        size=30,
        textlen=99,
        fontfile=font_file_path,
        text_color=draw_color("卡片标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (x + 20 + 25, y + 5))
    y += 40

    # 技能加点推荐
    y += 15
    paste_image = await draw_form(
        skll_data,
        size_x=int(image_x * 0.95),
        calculate=False,
        font_file_path=font_file_path
    )
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 18)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 15)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    return save_image(image, to_bytes=True)


async def draw_name(draw_data: dict):
    """
    绘制
    """
    image = Image.new("RGBA", (100, 100), (50, 50, 50, 255))

    return save_image(image, to_bytes=True)
