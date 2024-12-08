# coding=utf-8
from PIL import Image
from nonebot import logger, require
from .config import draw_color

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic
from .tools import save_image, load_image, draw_text, image_resize2, circle_corner, draw_form


async def draw_main(draw_data: dict, temp_name: str = None, temp_path: str = None):
    logger.debug(f"draw_data: {draw_data}")
    template_name = temp_path.split("/")[-1]
    logger.debug(f"template_path: {temp_path}")
    logger.debug(f"template_name: {template_name}")

    # 鸣潮角色查询
    if template_name == "rolecard":
        return await draw_rolecard(draw_data)
    # 鸣潮技能查询
    elif template_name == "":
        return await draw_name(draw_data)
    # 鸣潮共鸣链查询
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
            {"color": draw_color("群组名称"), "size": 30, "text": draw_data.get("attribute").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("attribute").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 30, "text": "特殊料理"},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("specialcuisine")},
        ], [
            {"color": draw_color("群组名称"), "size": 30, "text": draw_data.get("gender").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("gender").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 30, "text": "中文cv"},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("zhcv")},
        ], [
            {"color": draw_color("群组名称"), "size": 30, "text": draw_data.get("birthplace").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("birthplace").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 30, "text": "日文cv"},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("jpcv")},
        ], [
            {"color": draw_color("群组名称"), "size": 30, "text": draw_data.get("weapon").split("：")[0]},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("weapon").split("：")[1]},
            {},
            {"color": draw_color("群组名称"), "size": 30, "text": "英文cv"},
            {"color": draw_color("群组内容"), "size": 25, "text": draw_data.get("encv")},
        ], [
            {"color": draw_color("群组名称"), "size": 30, "text": "身份"},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("identity")},
            {},
            {"color": draw_color("群组名称"), "size": 30, "text": "韩文cv"},
            {"color": draw_color("群组内容"), "size": 25, "text": draw_data.get("kocv")},
        ], [
            {"color": draw_color("群组名称"), "size": 30, "text": "所属"},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("affiliation")},
            {},
            {"color": draw_color("群组名称"), "size": 30, "text": "实装版本"},
            {"color": draw_color("群组内容"), "size": 30, "text": draw_data.get("version")},
        ],
    ]
    combat_data = draw_data["combat_data"]
    forms_data_combat = [
        [
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[0][0]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[1][0]},
            {},
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[3][0]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[4][0]},
        ], [
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[0][1]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[1][1]},
            {},
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[3][1]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[4][1]},
        ], [
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[0][2]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[1][2]},
            {},
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[3][2]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[4][2]},
        ], [
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[0][3]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[1][3]},
            {},
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[3][3]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[4][3]},
        ], [
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[0][4]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[1][4]},
            {},
            {"color": draw_color("群组名称"), "size": 27, "text": combat_data[3][4]},
            {"color": draw_color("群组内容"), "size": 27, "text": combat_data[4][4]},
        ],
    ]
    image_x, image_y = (900, 0)
    image_y += 643  # 基础信息界面

    paste_image = await draw_form(forms_data_info, size_x=int(image_x * 0.95), calculate=True)
    image_y += paste_image.size[1]
    image_y += 20
    paste_image = await draw_form(forms_data_combat, size_x=int(image_x * 0.95), calculate=True)
    image_y += paste_image.size[1]

    image_y += 50  # 底部留空
    image = Image.new("RGBA", (image_x, image_y), (50, 50, 50, 255))

    # 开始绘制
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
        fontfile="优设好身体.ttf",
        text_color=draw_color("图标"),
        calculate=False
    )
    image.alpha_composite(paste_image, (25, 26))

    # 副图标
    paste_image = await draw_text(
        "wuthering waves",
        size=19,
        textlen=99,
        fontfile="优设好身体.ttf",
        text_color=draw_color("副图标"),
        calculate=False
    )
    image.alpha_composite(paste_image, (17, 60))

    # 标题-名称
    paste_image = await draw_text(
        draw_data.get("title"),
        size=72,
        textlen=99,
        fontfile="优设好身体.ttf",
        text_color=draw_color("标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 150))

    # 副标题-英文名称
    paste_image = await draw_text(
        draw_data.get("roleenname"),
        size=36,
        textlen=99,
        fontfile="优设好身体.ttf",
        text_color=draw_color("副标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 230))

    # 简介标题
    paste_image = await draw_text(
        draw_data.get("roleDescriptiontitle"),
        size=30,
        textlen=99,
        fontfile="优设好身体.ttf",
        text_color=draw_color("简介标题"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 346))

    # 简介内容
    paste_image = await draw_text(
        draw_data.get("roleDescription"),
        size=24,
        textlen=16,
        fontfile="优设好身体.ttf",
        text_color=draw_color("简介内容"),
        calculate=False
    )
    image.alpha_composite(paste_image, (38, 383))

    x = 0
    y = 643
    # 基础消息
    paste_image = await draw_form(forms_data_info, size_x=int(image_x * 0.95), calculate=False)
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 23)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 20)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))
    y += paste_image.size[1]

    # 战斗数据
    y += 20
    paste_image = await draw_form(forms_data_combat, size_x=int(image_x * 0.95), calculate=False)
    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 23)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 20)
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
