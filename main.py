from ya_api import *
from vk_api import *
id_vk = input("Введите ID VK.COM :")
token_yandex = input("Введите токен Яндекс :")

#Создаём папку на яндекс.диске
yandex_folder_creat("Photo_from_VK(AVATAR)")
#Получаем JSON от VK, формируем словарь (полная информация, без обработки)
# method/photos.get ('album_id':'profile')
dict_js_req = vk_response_avatar(id_vk)
#Обработка данных: вычленяем самое большое изображение, формируем имена, находим ссылки на файлы
#Функция возвращает {dict_name_link} - имена фалов и УРЛ фалов \ name = key \
dict_name_link = vk_response_processing(dict_js_req)

for photo in dict_name_link:
    link = dict_name_link[photo]
    yandex_upload(f"disk:/Photo_from_VK(AVATAR)/{photo}", link, token_yandex)

