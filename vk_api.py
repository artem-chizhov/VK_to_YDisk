import requests
from pprint import pprint
from _bar_ import *

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

def vk_response_processing(js_req):
    #Количество записей в json, который вернулся с VK
    count = js_req["response"]["count"]
    like_list = []
    result = []
    dict_name_link = {}
    for photo in range(count):
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
        if photo+1 == count:
            print("Обработка закончена")
        else:
            print("Переходим к следующей аватарке")
        progress_bar_stop()
    #Записываем данные(список словарей - имя файла + размер) в json файл (корневая директория)
    progress_bar(f'Формируем файл result.json...:', 1)
    with open('result.json','a') as document:
        document.write(f'{result}\n')
    progress_bar_stop()
    print("===="*20)
    pprint(result)
    print("===="*20)
    return dict_name_link