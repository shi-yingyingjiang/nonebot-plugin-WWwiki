# coding=utf-8
from PIL import Image
from nonebot import logger, require
from .config import draw_color

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic
from .tools import save_image, load_image, draw_text, image_resize2, circle_corner


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
    image_x, image_y = (900, 0)
    image_y += 643  # 基础信息界面

    paste_image = await draw_form(forms_data_info, size_x=int(image_x * 0.95), calculate=True)
    image_y += paste_image.size[1]

    image_y += 50  # 底部留空
    image = Image.new("RGBA", (image_x, image_y), (50, 50, 50, 255))

    # 开始绘制
    # 立绘
    paste_image = await load_image(draw_data.get("roleimg"))
    image.alpha_composite(paste_image, (263, -57))

    # 角色logo
    paste_image = await load_image(draw_data.get("campIcon"))
    paste_image = image_resize2(paste_image, (128, 128))
    image.alpha_composite(paste_image, (745, 22))

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

    # 消息栏
    x = 0
    y = 643
    paste_image = await draw_form(forms_data_info, size_x=int(image_x * 0.95), calculate=False)

    paste_card = Image.new("RGBA", (int(image_x * 0.95) + 6, paste_image.size[1] + 6), draw_color("卡片描边"))
    paste_card = circle_corner(paste_card, 23)
    image.alpha_composite(paste_card, (int(image_x * 0.025) - 3, y - 3))
    paste_card = Image.new("RGBA", (int(image_x * 0.95), paste_image.size[1]), draw_color("卡片背景"))
    paste_card = circle_corner(paste_card, 20)
    image.alpha_composite(paste_card, (int(image_x * 0.025), y))
    image.alpha_composite(paste_image, (int(image_x * 0.025), y))

    return save_image(image, to_bytes=False)


async def draw_form(form_data: list, size_x: int, calculate: bool = False) -> Image.Image:
    """
    绘制表格
    :param form_data: 表格数据
    :param size_x: x的尺寸
    :param calculate: 是否仅计算不绘制
    :return:保存的路径
    """
    size_y = 0
    size_y += 16
    for form_x in form_data:
        add_size_y = 0
        for form_y in form_x:
            if form_y.get("text") is None:
                continue
            draw_size = await draw_text(
                form_y.get("text"),
                size=form_y["size"],
                textlen=int(size_x / len(form_x) / form_y["size"]),
                fontfile="优设好身体.ttf",
                text_color=form_y.get("color"),
                calculate=True
            )
            draw_size = draw_size.size[1]
            if draw_size > add_size_y:
                add_size_y = draw_size
        size_y += add_size_y
        size_y += 11
        size_y += 6
    size_y += 16

    image = Image.new("RGBA", (size_x, size_y), (0, 0, 0, 0))
    if calculate is True:
        return image

    paste_line = Image.new("RGBA", (int(size_x * 0.95), 3), draw_color("卡片分界线"))
    num_y = -1
    for form_x in form_data:
        num_y += 1
        num_x = -1
        if num_y != 0:
            image.alpha_composite(paste_line, (int(size_x * 0.025), int(num_y * size_y / len(form_data))))

        for form_y in form_x:
            num_x += 1
            if form_y.get("text") is None:
                continue
            paste_image = await draw_text(
                form_y.get("text"),
                size=form_y["size"],
                textlen=int(size_x / len(form_x) / form_y["size"]),
                fontfile="优设好身体.ttf",
                text_color=form_y.get("color"),
                calculate=False
            )
            image.alpha_composite(paste_image, (
                int(num_x * size_x / len(form_x) + (size_x * 0.01)),
                int((num_y * size_y / len(form_data)) + (((size_y / len(form_data)) - paste_image.size[1]) / 2))
            ))

    return image


async def draw_name(draw_data: dict):
    """
    绘制
    """
    image = Image.new("RGBA", (100, 100), (50, 50, 50, 255))

    return save_image(image, to_bytes=True)
