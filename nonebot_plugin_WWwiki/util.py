from pathlib import Path

from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")

from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_htmlrender import html_to_pic, get_new_page, template_to_pic


__dir = Path(__file__).parent.resolve().absolute()

html_templates = __dir / "html_template"


__all__ = ["UniMessage", "html_to_pic", "get_new_page", "html_templates", "template_to_pic"]
