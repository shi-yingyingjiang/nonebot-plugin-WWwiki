# coding=utf-8
import io
import json
import platform
import shutil
import httpx
from PIL.Image import Image as PIL_Image
from PIL import Image, ImageDraw, ImageFont
import random
from nonebot import logger
import os
import time
from .config import basepath


def save_image(
        image,
        image_path: str = None,
        image_name: int | str = None,
        relative_path=False,
        to_bytes: bool = False):
    """
    保存图片文件到缓存文件夹
    :param image:要保存的图片
    :param image_path: 指定的图片所在文件夹路径，默认为缓存
    :param image_name:图片名称，不填为随机数字
    :param relative_path: 是否返回相对路径
    :param to_bytes: 是否转为bytes
    :return:保存的路径
    """
    image = image.convert("RGB")
    if to_bytes is True and type(image) is PIL_Image:
        # 将Pillow图像数据保存到内存中
        image_stream = io.BytesIO()
        image.save(image_stream, format='JPEG')
        image_stream.seek(0)
        return image_stream.read()

    d_y, d_m, d_d = map(int, time.strftime("%Y/%m/%d", time.localtime()).split("/"))
    time_now = int(time.time())

    if image_path is None:
        image_path = "{basepath}" + f"cache/{d_y}/{d_m}/{d_d}/"
    real_path = image_path.replace("{basepath}", basepath)
    os.makedirs(real_path, exist_ok=True)

    if image_name is None:
        image_name = f"{time_now}_{random.randint(1000, 9999)}"
        num = 50
        while True:
            num -= 1
            random_num = str(random.randint(1000, 9999))
            if os.path.exists(f"{real_path}{image_name}_{random_num}.jpg"):
                continue
            image_name = f"{image_name}_{random_num}.jpg"
            break

    logger.debug(f"保存图片文件：{real_path}{image_name}")
    image.save(f"{real_path}{image_name}")

    if to_bytes is True:
        image_file = open(f"{real_path}{image_name}", "rb")
        image = image_file.read()
        image_file.close()
        return image
    if relative_path is True:
        return f"{image_path}{image_name}"
    else:
        return f"{real_path}{image_name}"


def circle_corner(img, radii: int):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """

    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img


def image_resize2(image, size: [int, int], overturn=False):
    """
    重缩放图像
    :param image: 要缩放的图像
    :param size: 缩放后的大小
    :param overturn: 是否放大到全屏
    :return: 缩放后的图像
    """
    image_background = Image.new("RGBA", size=size, color=(0, 0, 0, 0))
    image_background = image_background.resize(size)
    w, h = image_background.size
    x, y = image.size
    if overturn:
        if w / h >= x / y:
            rex = w
            rey = int(rex * y / x)
            paste_image = image.resize((rex, rey))
            image_background.paste(paste_image, (0, 0))
        else:
            rey = h
            rex = int(rey * x / y)
            paste_image = image.resize((rex, rey))
            x = int((w - rex) / 2)
            image_background.paste(paste_image, (x, 0))
    else:
        if w / h >= x / y:
            rey = h
            rex = int(rey * x / y)
            paste_image = image.resize((rex, rey))
            x = int((w - rex) / 2)
            y = 0
            image_background.paste(paste_image, (x, y))
        else:
            rex = w
            rey = int(rex * y / x)
            paste_image = image.resize((rex, rey))
            x = 0
            y = int((h - rey) / 2)
            image_background.paste(paste_image, (x, y))

    return image_background


async def draw_text(
        texts: str,
        size: int,
        textlen: int = 20,
        fontfile: str = "",
        text_color="#000000",
        calculate=False
):
    """
    - 文字转图片
    :param texts: 输入的字符串
    :param size: 文字尺寸
    :param textlen: 一行的文字数量
    :param fontfile: 字体文字
    :param text_color: 字体颜色，例："#FFFFFF"、(10, 10, 10)
    :param calculate: 计算长度。True时只返回空白图，不用粘贴文字，加快速度。

    :return: 图片文件（RGBA）
    """
    if texts is None:
        texts = "None"

    def get_font_render_w(text):
        if text == " ":
            return 20
        none = ["\n", ""]
        if text in none:
            return 1
        canvas = Image.new('RGB', (500, 500))
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), text, font=font, fill=(255, 255, 255))
        bbox = canvas.getbbox()
        # 宽高
        # size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        if bbox is None:
            return 0
        return bbox[2]

    default_font = ["msyh.ttc"]
    size = size
    if fontfile == "":
        fontfile = "msyh.ttc"
    if not fontfile.startswith("/") or ":/" in fontfile:
        # 获取字体绝对路径
        font_list = [fontfile] + default_font + ["no_font"]
        os_name = platform.system()
        for font in font_list:
            if font == "no_font":
                logger.error(f"字体加载失败，请安装字体{font_list[0]}")
                raise f"字体加载失败，请安装字体"
            if os_name.lower() == 'windows':
                if os.path.exists(f"C:/Windows/Fonts/{font}"):
                    fontfile = f"C:/Windows/Fonts/{font}"
                else:
                    fontfile = f"C:/Users/{os.getlogin()}/AppData/Local/Microsoft/Windows/Fonts/{font}"
            elif os_name.lower() == 'linux':
                fontfile = f"/usr/share/fonts/{font}"
            else:
                print(f"当前操作系统为 {os_name}")
            if os.path.exists(fontfile):
                break

    font = ImageFont.truetype(font=fontfile, size=size)

    # 计算图片尺寸
    print_x = 0
    print_y = 0
    jump_num = 0
    text_num = -1
    for text in texts:
        text_num += 1
        if jump_num > 0:
            jump_num -= 1
        else:
            if (textlen * size) < print_x or text == "\n":
                print_x = 0
                print_y += 1.3 * size
                if text == "\n":
                    continue
            if text in ["\n", " "]:
                if text == " ":
                    print_x += get_font_render_w(text) + 2
            else:
                print_x += get_font_render_w(text) + 2

    x = int((textlen + 1.5) * size)
    y = int(print_y + 1.2 * size)

    image = Image.new("RGBA", size=(x, y), color=(0, 0, 0, 0))  # 生成透明图片
    draw_image = ImageDraw.Draw(image)

    # 绘制文字
    if calculate is False:
        print_x = 0
        print_y = 0
        jump_num = 0
        text_num = -1
        for text in texts:
            text_num += 1
            if jump_num > 0:
                jump_num -= 1
            else:
                if (textlen * size) < print_x or text == "\n":
                    print_x = 0
                    print_y += 1.3 * size
                    if text == "\n":
                        continue
                if text in ["\n", " "]:
                    if text == " ":
                        print_x += get_font_render_w(text) + 2
                else:
                    draw_image.text(xy=(int(print_x), int(print_y)),
                                    text=text,
                                    fill=text_color,
                                    font=font)
                    print_x += get_font_render_w(text) + 2
        # 把输出的图片裁剪为只有内容的部分
        bbox = image.getbbox()
        if bbox is None:
            box_image = Image.new("RGBA", (2, size), (0, 0, 0, 0))
        else:
            box_image = Image.new("RGBA", (bbox[2] - bbox[0], bbox[3] - bbox[1]), (0, 0, 0, 0))
            box_image.paste(image, (0 - int(bbox[0]), 0 - int(bbox[1])), mask=image)
        image = box_image
    return image


async def load_image(path: str, size=None, mode=None, cache_image=True):
    """
    读取图片或请求网络图片
    :param path: 图片路径/图片url
    :param size: 出错时候返回的图片尺寸
    :param mode: 图片读取模式
    :return:image
    """
    if mode is None:
        mode = "r"
    try:
        if path.startswith("http"):
            if cache_image is False:
                image = await connect_api("image", path)
            else:
                cache_path = path.removeprefix("http://").removeprefix("https://").split("?")[0]

                if os.path.exists(f"{basepath}cache/web_cache/{cache_path}"):
                    return Image.open(f"{basepath}cache/web_cache/{cache_path}")
                file_name = cache_path.split("/")[-1]
                file_path = f"{basepath}cache/web_cache/{cache_path.removesuffix(file_name)}"
                os.makedirs(file_path, exist_ok=True)
                image = await connect_api("image", path)
                image.save(f"{file_path}{file_name}")

            return image
        else:
            if path.startswith("{basepath}"):
                image_path = path.replace("{basepath}", basepath)
                if not os.path.exists(image_path):
                    raise "图片不存在"
                image = Image.open(image_path, mode)
                if mode == "rb":
                    return save_image(image, to_bytes=True)
                return image
            return Image.open(path, mode)
    except Exception as e:
        logger.error(f"读取图片错误：{path}")
        logger.error(e)
        if size is not None:
            return Image.new("RGBA", size, (0, 0, 0, 0))
        raise "图片读取错误"


async def connect_api(
        connect_type: str,
        url: str,
        post_json=None,
        file_path: str = None,
        timeout: int = 10
):
    logger.debug(f"connect_api请求URL：{url}")
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"}
    if connect_type == "json":
        if post_json is None:
            async with httpx.AsyncClient() as client:
                data = await client.get(url, headers=h, timeout=timeout)
            return json.loads(data.text)
        else:
            async with httpx.AsyncClient() as client:
                data = await client.post(url, json=post_json, headers=h, timeout=timeout)
            return json.loads(data.text)
    elif connect_type == "image":
        if url is None or url in ["none", "None", "", " "]:
            image = await draw_text("获取图片出错", 50, 10)
        else:
            try:
                async with httpx.AsyncClient() as client:
                    data = await client.get(url, timeout=timeout)
                image = Image.open(io.BytesIO(data.content))
            except Exception as e:
                logger.error(e)
                logger.error(url)
                raise "获取图片出错"
        return image
    elif connect_type == "file":
        cache_file_path = file_path + "cache"
        f = open(cache_file_path, "wb")
        try:
            res = httpx.get(url, headers=h, timeout=timeout).content
            f.write(res)
            logger.debug(f"下载完成-{file_path}")
        except Exception as e:
            logger.error(e)
            raise Exception
        finally:
            f.close()
        shutil.copyfile(cache_file_path, file_path)
        os.remove(cache_file_path)
    return
