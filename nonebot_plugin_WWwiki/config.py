# coding=utf-8
from pathlib import Path
import json
from typing import Dict, List


group_data = Path()/"data"/"WWwiki"/"groupid.json"
group_data.parent.mkdir(parents=True, exist_ok=True)
if not group_data.exists():
    CONFIG: Dict[str, List] = {"opened_groups": []}
    with open(group_data, "w", encoding="utf8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)