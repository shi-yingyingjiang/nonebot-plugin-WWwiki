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
            _basepath = os.path.abspath('.') + "/WWwiki/pil_draw/"

    except Exception as e:
        _basepath = os.path.abspath('.') + "/KanonBot/"

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


_config = _plugin_config()
basepath = _config["basepath"]
