
from _bar_ import *
import pprint
#Записываем данные(список словарей - имя файла + размер) в json файл (корневая директория)
def creat_log_file(result):
    name_file_log = input("Введите название лог файла : ")
    progress_bar(f'Формируем файл {name_file_log}.json...:', 1)
    with open(f'{name_file_log}.json','a') as document:
        document.write(f'{result}\n')
    progress_bar_stop()
    print("===="*20)
    pprint(result)
    print("===="*20)