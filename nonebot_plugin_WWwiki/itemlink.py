# coding=utf-8
import httpx
import json

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
rolelisturl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getPage'


def is_value_in_dicts_list(dict_list, key, value):
    """判断给定的值是否在列表中任意字典的指定键的值中存在"""
    for dictionary in dict_list:
        if value == dictionary.get(key):  # 使用get方法避免键不存在时抛出错误
            return True
    return False


# 示例用法


async def get_link(name, listdata):
    async with httpx.AsyncClient() as client:

        res = await client.post(rolelisturl, data=listdata, headers=headers)
        role_list = json.loads(res.text)
        records = role_list.get('data').get('results').get('records')
        key_to_check = "name"
        value_to_check = name
        if is_value_in_dicts_list(records, key_to_check, value_to_check):
            matching_entryIds = [item['entryId'] for item in records if item['name'] == name]
        else:
            matching_entryIds = None
        return matching_entryIds



async def classify(thetitle, listdata):
    async with httpx.AsyncClient() as client:
        res = await client.post(rolelisturl, data=listdata, headers=headers)
        data = json.loads(res.text)
        tagtree = data['data']['tagTree']['children'][3]['children']
        records = data['data']['results']['records']


        
        target_value = None

        # 在tagtree中查找search_value对应的id
        for d in tagtree:
            if d.get('name') == thetitle:
                target_value = d.get('id')
                break

        # 只有当target_value被成功赋值时，才执行下面的逻辑
        if target_value is not None:
            results = []
            for record in records:
                if str(target_value) in record["content"]["relateTagIds"]:
                    title = record["content"]["title"]
                    content_url = record["content"]["contentUrl"]
                    results.append({"title": title, "contentUrl": content_url})
        else:
            results = None
            name_list = [d['name'] for d in tagtree]
            thetitle = '\n'.join(name_list)

        return results,thetitle
        