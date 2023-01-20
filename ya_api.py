import requests
from _bar_ import *


def yandex_get_headers(token):
    return{
        'Content-Type':'application/json',
        'Authorization':f'OAuth {token}'
    }

def yandex_folder_creat(disk_folder_path: str, token):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = yandex_get_headers(token)
    params = {"path":disk_folder_path}
    response = requests.put(upload_url, headers=headers, params=params)
    if str(response.status_code) == "409":
        print("Папка существует, продолжаем работу.")
    elif str(response.status_code) == "201":
        print("Папка создана, продолжаем работу...")
    else:
        print(response.status_code)
    return response

def yandex_upload(file_path:str, url_path:str, token):
    headers = yandex_get_headers(token)
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    params = {"path":file_path, "url":url_path}
    response = requests.post(upload_url, headers = headers, params = params)
    name = file_path.split("/")
    progress_bar("Записываем файл на Я.Диск...:", 1)
    if response.status_code == 202:
        print(f"Файл {name} загружен на Я.Диск!")
    else:
        print(response.status_code)
        print(response.reason)
    progress_bar_stop()
