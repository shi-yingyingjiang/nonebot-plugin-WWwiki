# coding=utf-8


def get_basic_information(data):
    role_name = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('title')
    role_img = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('figures')[0].get('url')
    role_description = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('roleDescription')
    role_description_title = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('roleDescriptionTitle')
    info_data = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')
    while len(info_data) < 6:
        info_data.append({"text": "none"})

    info = [item["text"] for item in info_data[:6]]
    role_gender = info[0]
    birthplace = info[1]
    weapon = info[2]
    attribute = info[3]
    role_en_name = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('subtitle')
    campIcon = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('campIcon')

    return {
        'role_name': role_name,
        'role_img': role_img,
        'role_en_name' : role_en_name,
        'role_description': role_description,
        'role_description_title': role_description_title,
        'role_gender': role_gender,
        'attribute': attribute,
        'weapon': weapon,
        'birthplace': birthplace,
        'campIcon' : campIcon
    }
