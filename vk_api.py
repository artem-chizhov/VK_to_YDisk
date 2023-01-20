import requests
from pprint import pprint
from _bar_ import *
import os
from dotenv import load_dotenv, find_dotenv
from create_log_file import *

def vk_user_get(user_id):
    version='5.131'
    load_dotenv(find_dotenv())
    token = os.getenv('TOKEN_VK')
    url = 'https://api.vk.com/method/users.get'
    params = {'user_ids': user_id,
            'access_token': token,
            'v': version
            }
    response = requests.get(url, params={**params})
    return response.json()


def vk_response_avatar(user_id):
    version='5.131'
    token = ''
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': user_id,
            'access_token': token,
            'v': version,
            'album_id':'profile',
            'extended': '1',
            'photo_sizes':'1',
            'count':'5'}
    response = requests.get(url, params={**params})
    return response.json()

def vk_screen_name(user_id):
    version = '5.131'
    load_dotenv(find_dotenv())
    token = os.getenv('TOKEN_VK')
    url = 'https://api.vk.com/method/utils.resolveScreenName'
    params = {
            'access_token': token,
            'screen_name': user_id,
            'v': version
    }
    response = requests.post(url, params={**params})
    return response.json()

def vk_response_processing(js_req):
    #Количество записей в json, который вернулся с VK
    count = js_req["response"]["count"]
    try:
        count_user = int(input(f"""
                    Количество найденых фотографий = {count}, 
                    Укажите количество выгружаемых фото : 
                    """))
    except:
        print("Возможны только целочисленные значения! Выгружаем все фото!")
        count_user = count
    if count > count_user:
        print("Введенное количество больше доступного! Выгружаем все фото!")
    like_list = []
    result = []
    dict_name_link = {}
    for photo in range(count_user):
        progress_bar(f'Формируем данные аватарки №{photo+1}', 1)
        #проверяем наличие имени (именем является количество лайков) в списке
        if js_req["response"]["items"][photo]["likes"]["user_likes"] in like_list:
            #Если да - присваиваем переменной "date" (именем файла будет являться дата)
            file_name = js_req["response"]["items"][photo]['date']
        else:
            #Если нет - добавляем в список имя (именем является количество лайков) в список
            like_list.append(js_req["response"]["items"][photo]["likes"]["user_likes"])
            #Переменной присваиваем имя - количество лайков
            file_name = js_req["response"]["items"][photo]["likes"]["user_likes"]
        print(f"\nФайлу присвоено имя: {file_name}")
        #Вытаскиваем ссылку на картинку
        file_link = js_req["response"]["items"][photo]["sizes"][0]["url"]
        print(f"...Забрали URL файла....")
        #сохраняем расширение файла в переменную
        exp = file_link.split("?size")[0].split(".")[-1]
        #сохраняем значение "sizes" (картинка бОльшего размера)
        size = js_req["response"]["items"][photo]["sizes"][-1]["type"]
        print("...Нашли самое большое изображение...")
        #формируем список словарей - имя файла + размер
        result.append({
            "file_name": f"{file_name}.{exp}",
            "size": size
            })
        #формируем словарь - имя файла : ссылка на картинку
        dict_name_link[f"{file_name}.{exp}"] = file_link
        if photo+1 == count_user:
            print("Обработка закончена")
        else:
            print("Переходим к следующей аватарке")
        progress_bar_stop()
    #Записываем данные(список словарей - имя файла + размер) в json файл (корневая директория)
    creat_log_file(result)
    return dict_name_link

def vk_check_gr_or_user(id_cname):
    id = None
    while True:
        screen_name = vk_screen_name(id_cname)['response']
        user_get_name = vk_user_get(id_cname)['response']
        if screen_name == [] and user_get_name == []:
            print("Совпадений нет! Проверьте вводимые данные!")
            break
        elif screen_name == [] and user_get_name != []:
            print(f"Найден пользователь ВК! -> {user_get_name[0]['first_name']}")
            id = id_cname
            break
        elif user_get_name == [] and screen_name != []:
            print(f"Нашли {screen_name['type']} с ID {screen_name['object_id']} и коротким именем {id_cname}")
            id = screen_name['object_id']
            break
        elif user_get_name[0]['id'] == screen_name['object_id']:
            id = id_cname
            break
        else:
            while True:
                double = input(f"""
                    Существует {screen_name['type']} с ID {screen_name['object_id']}
                    и Существует юзер {user_get_name[0]['first_name']} с ID {user_get_name[0]['id']}
                    Уточните какие данные используем пользователь (U) или {screen_name['type']} (T)
                    :
                    """)
                if double.upper() == 'U':
                    id = user_get_name[0]['id']
                    break
                elif double.upper() == 'T':
                    id = screen_name['object_id']
                    break
                else:
                    print("Доступны только перечисленные значения для ввода: u,U,t,T")
                    continue
            break  
    return id