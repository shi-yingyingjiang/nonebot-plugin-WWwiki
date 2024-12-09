# coding=utf-8
import os
import nonebot


def _plugin_config():
    # 读取配置
    # -》无需修改代码文件，请在“.env”文件中改。《-
    #
    # 配置1：
    # 文件存放目录
    # 该目录是存放插件数据的目录，参考如下：
    # plugin_wwwiki_basepath="./"
    # plugin_wwwiki_basepath="C:/nonebot/"
    # 默认："./WWwiki/pil_draw/"

    # 读取配置文件
    try:
        config = nonebot.get_driver().config
        # 配置1
        try:
            _basepath = config.plugin_wwwiki_basepath
        except Exception as e:
            _basepath = os.path.abspath('.') + "/data/WWwiki/pil_draw/"
    except Exception as e:
        _basepath = os.path.abspath('.') + "/data/WWwiki/pil_draw/"

    if "\\" in _basepath:
        _basepath = _basepath.replace("\\", "/")
    if not _basepath.endswith("/"):
        _basepath += "/"
    if _basepath.startswith("./"):
        _basepath = os.path.abspath('.') + _basepath.removeprefix(".")

    # 初始化文件夹
    os.makedirs(f"{_basepath}cache/", exist_ok=True)
    os.makedirs(f"{_basepath}file/", exist_ok=True)
    os.makedirs(f"{_basepath}image/", exist_ok=True)

    return {
        "basepath": _basepath,
    }


def draw_color(name: str):
    color_data = {
        "背景": "#323232",
        "背景图片": None,
        "图标": "#e0c698",
        "副图标": "#c5c2bc",
        "标题": "#fff6e6",
        "副标题": "#c19f64",
        "简介标题": "#e1e1e1",
        "简介内容": "#a1a1a1",
        "卡片标题": "#feedcd",
        "卡片标题背景": "#bea77b",
        "卡片背景": "#434343",
        "卡片描边": "#e0c698",
        "卡片分界线": "#7c7363",
        "群组标题": "#",
        "群组副标题": "#",
        "群组名称": "#b49254",
        "群组内容": "#e1e1e1",
    }
    if name not in color_data.keys():
        raise "颜色不在配色中"
    if color_data[name] == "#":
        return "#000000"
    return color_data[name]


_config = _plugin_config()
basepath = _config["basepath"]
