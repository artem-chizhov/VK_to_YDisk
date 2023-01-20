from ya_api import *
from vk_api import *
#Запрашивается вариация ID или screen_name, так как в ВК существуют группы с коротким именем например "777" которые имеют свой ID. имеет 
#question = input("Выберете вариант подключения - ID или короткое имя :")
#vk_sc_name = input("Введите короткое имя :")
while True:    
    id_vk = input("Введите ID VK.COM или короткое имя :")
    id_vk = vk_check_gr_or_user(id_vk)
    if id_vk != None:
        break
    else:
        continue

token_yandex = input("Введите токен Яндекс :")

#Создаём папку на яндекс.диске
folder_yandex = input("Введите желаемое имя папки на яндекс диске ")
yandex_folder_creat(folder_yandex, token_yandex)
#Получаем JSON от VK, формируем словарь (полная информация, без обработки)
# method/photos.get ('album_id':'profile')
dict_js_req = vk_response_avatar(id_vk)
#Обработка данных: вычленяем самое большое изображение, формируем имена, находим ссылки на файлы
#Функция возвращает {dict_name_link} - имена фалов и УРЛ фалов \ name = key \
print(dict_js_req)
dict_name_link = vk_response_processing(dict_js_req)

for photo in dict_name_link:
    link = dict_name_link[photo]
    yandex_upload(f"disk:/{folder_yandex}/{photo}", link, token_yandex)

