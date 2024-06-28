import json



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
    role_birthday = info[1]
    attribute = info[2]
    weapon = info[3]
    affiliation = info[4]
    birthplace = info[5]
    role_en_name = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('subtitle')
    campIcon = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('campIcon')



    return{
        'role_name': role_name,
        'role_img': role_img,
        'role_en_name' : role_en_name,
        'role_description': role_description,
        'role_description_title': role_description_title,
        'role_gender': role_gender,
        'role_birthday': role_birthday,
        'attribute': attribute,
        'weapon': weapon,
        'affiliation': affiliation,
        'birthplace': birthplace,
        'campIcon' : campIcon
    }


