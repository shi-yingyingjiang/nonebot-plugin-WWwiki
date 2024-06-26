import json



def get_basic_information(data):
    role_name = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('title')
    role_img = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('figures')[0].get('url')
    role_description = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('roleDescription')
    role_description_title = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('roleDescriptionTitle')
    role_gender = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')[0].get('text')
    role_birthday = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')[1].get('text')
    attribute = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')[2].get('text')
    weapon = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')[3].get('text')
    affiliation = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')[4].get('text')
    birthplace = data.get('data').get('content').get('modules')[0].get('components')[0].get('role').get('info')[5].get('text')
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


