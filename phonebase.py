# Создать телефонный справочник с возможностью импорта и экспорта данных в формате .txt.
# Структура данных:
# Фамилия, имя, отчество, номер телефона.
# Пример данных:
# Ivanov, Ivan, Ivanovich, +79111234567
# Petrov, Petr, Petrovich, +79119876543
# Функции справочника:
# - Показать все записи
# - Найти запись по вхождению частей имени
# - Найти запись по телефону
# - Добавить новый контакт
# - Удалить контакт
# - Изменить номер телефона у контакта
# Пример работы программы:
# При запуске программы пользователю выдается меню:
# Введите номер действия:
# 1 - Показать все записи
# 2 - Найти запись по вхождению частей имени
# 3 - Найти запись по телефону
# 4 - Добавить новый контакт
# 5 - Удалить контакт
# 6 - Изменить номер телефона у контакта
# 7 - Выход
# После выбора действия выполняется функция, реализующая это действие.
# После завершения работы функции пользователь возвращается в меню.
import os
from sys import platform
import re 

#функция для очистки экрана
def clear_screen():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")  # для Linux & MacOS
    else:
        os.system("cls")    # для Windows

#функция для отображения содержимого справочника

def showAll(name):
    clear_screen()
    with open(name, 'r', encoding='UTF-8') as f:
        counter = 0
        for item in f:
            counter += 1
            print(counter, *item.strip().split(','))
        print(f'Всего найдено записей: {counter}')

#выход из справочника
def Exit(name):
    clear_screen()
    print('До свидания! Хорошего дня)')
    return -1

#поиск по имени
def findByName(name):
        clear_screen()
        while True:
            try:
                string = input("Введите ФИО или часть ФИО >>> ").replace(' ', '')
                if string.isalpha():
                    dataFind = {}      
                    counter = 0
                    with open(name, 'r', encoding='UTF-8') as f:
                        for item in f:
                            if string.lower() in item.lower().replace(',', ''):
                                counter += 1
                                dataFind[counter] = item
                                print(counter, dataFind[counter].replace(',', ' ').rstrip())
                        if counter == 0:
                            print("Совпадений не найдено, попробуйте изменить запрос")
                        else:
                            print(f'Всего найдено записей: {counter}') 
                            return dataFind
                else:
                    raise Exception
                    
            except: print('Введены некорректные данные, попробуйте еще раз!')

#поиск по номеру телефона
def findByPhone(name):
    clear_screen()
    while True:
        try:
            number = input("Введите номер телефона или часть номера без кода +7>>> ")
            if number.isdigit():      
                counter = 0
                with open(name, 'r', encoding='UTF-8') as f:
                    for item in f:
                        if number in item:
                            counter += 1
                            print(*item.strip().split(','))
                    if counter == 0:
                        print("Совпадений не найдено, попробуйте изменить запрос")
                    else:
                        print(f'Всего найдено записей: {counter}')
                        break
            else:
                raise Exception    
        except: print('Введены некорректные данные, попробуйте еще раз!')

#ввод корректного номера
def correctNumber():
    while True:
        pattern = r'\b\+?[7,8]?(\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b'
        try:
            num = input("Введите номер телефона >>> ")
            number = re.findall(pattern, num)
            if number[0]:
                return '+7' + number[0][-10:]
            else: raise Exception
        except: print('Номер введен некорректно, попробуйте еще раз')

#ввод корректного имени
def correctName(text):
    while True:
        pattern = r'[а-яёА-ЯЁ]{2,}'
        try:
            word = input(f"Введите {text} >>> ")
            Name = re.findall(pattern, word)
            if Name:
                return Name[0].capitalize()
            else: raise Exception
        except: print('Имя введено некорректно, попробуйте еще раз')

#добавление нового контакта
def addNewContact(name):
    clear_screen()
    with open(name, 'a+', encoding='UTF-8') as out:
        lastname = correctName('Фамилию')
        firstname = correctName('Имя')
        fathername = correctName('Отчество')
        phone = correctNumber() 
        print(lastname, firstname, fathername, phone, sep=',', end='\n', file=out)
        print('Контакт успешно добавлен!')

#подтверждение выбора
def yesnoChoice(Name, operation = 'удалить'):
    while True:
        try:
            n = Name.replace(',', ' ')
            answer = input(f'Нажмите Y если хотите {operation} контакт  {n[:-13]}\n Нажмите N - чтобы отменить команду {operation}\n >>> ')
            if answer in ['Y', 'y']:
                return True
            elif answer in ['N', 'n']:
                print(f'Команда {operation} отменена')
                return False
            else:
                raise Exception
        except: print('Некорректный ввод, повторите выбор')    

#удаление строки из справочника
def delString(name, file):
    with open(file, 'r', encoding='UTF-8') as f:
        lines = [i for i in f.readlines() if i != name]
    with open(file, 'w', encoding='UTF-8') as f:
        for line in lines:
            f.write(line)
        print('\nКонтакт успешно удален!')

#удалить контакт после поиска по имени в книге с подтверждением
def deleteContact(name):
    clear_screen()
    res = findByName(name)
    if len(res) == 1:
        if yesnoChoice(res[1]):
            delString(res[1], name)
    elif len(res) > 1:
        print('Выберите порядковый номер контакта, который хотите удалить >>> ')
        while True:
            try: 
                num = int(input())
                if num in res:
                    if yesnoChoice(res[num]):
                        delString(res[num], name)
                        break
                    else:
                        main()
                else: 
                    raise Exception
            except:
                print("Введен некорректный номер, попробуйте еще раз")

#изменение строки в справочнике
def changeString(name, num, file):
    with open(file, 'r', encoding='UTF-8') as f:
        lines = [i if i != name else (i[:-13]+num+'\n') for i in f.readlines()]
    with open(file, 'w', encoding='UTF-8') as f:
        for line in lines:
            f.write(line)
        print('\nКонтакт успешно отредактирован!')

#изменение номера в книге с подтверждением
def ChangeNumber(name):
    clear_screen()
    print('Чей телефон будем редактировать?')
    res = findByName(name)
    if len(res) == 1:
        print('Укажите новый номер телефона')
        n = correctNumber()
        if yesnoChoice(res[1], 'редактировать'):
            changeString(res[1], n, name)
    elif len(res) > 1:
        print('Выберите порядковый номер контакта, который будем редактировать >>> ')
        while True:
            try: 
                num = int(input())
                if num in res:
                    print('Укажите новый номер телефона')
                    n = correctNumber()
                    if yesnoChoice(res[num], 'редактировать'):
                        changeString(res[num], n, name)
                        break
                    else:
                        main()
                else: 
                    raise Exception
            except:
                print("Введен некорректный номер, попробуйте еще раз")

menu = {'1':  showAll,\
'2': findByName,
'3': findByPhone,
'4': addNewContact,
'5': deleteContact,
'6': ChangeNumber,
'7': Exit}

name = 'phonebook.txt'

#основная программа  

def main():
    while True:
        try:
            print('''
Введите номер действия:
1 - Показать все записи
2 - Найти запись по вхождению частей имени
3 - Найти запись по телефону
4 - Добавить новый контакт
5 - Удалить контакт
6 - Изменить номер телефона у контакта
7 - Выход''')
            func = menu[input("Номер >>> ")]
            a = func(name)
            if a == -1:
                break
        except:
            print("Вы ввели некорректный номер, попробуйте еще раз")
            
main()
