# coding=utf-8
from pathlib import Path
import json
from typing import Dict, List, Literal
from nonebot import get_plugin_config
from pydantic import BaseModel


group_data = Path()/"data"/"WWwiki"/"groupid.json"
group_data.parent.mkdir(parents=True, exist_ok=True)
if not group_data.exists():
    CONFIG: Dict[str, List] = {"opened_groups": []}
    with open(group_data, "w", encoding="utf8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)


class Config(BaseModel):
    # 发送信息的模式
    makeimg_mode: Literal['htmltopic', 'piltopic'] = 'htmltopic'


plugin_config = get_plugin_config(Config)