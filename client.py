import requests
from models import User, Message
import sys
import re
from datetime import datetime

user=None
contacts=[]


def first_menu():
    '''First menu that allows user to sing in or loging'''
    next_menu=0

    while True:
        try:

            next_menu=int(input("""Здравствуйте! Добро пожаловать в чат!
Выберите пункт меню:
1 - Войти в существующую учетную запись
2 - Зарегестрироваться
3 - Выход
Ваш выбор >>> """))
            if next_menu in range(1,4):
                break
            else:
                print("Неверный Ввод. Пожалуйста, введите коректное число.")
                continue
        except:
            print("Неверный Ввод. Пожалуйста, введите коректное число.")
            continue
    if next_menu == 1:
        log_in()
    elif next_menu == 2:
        sing_in()
    else: 
        print("Спасибо, что воспользовались нашим приложением!")
        sys.exit()

def log_in():
    ''' Loging in to chat'''
    nickname =''
    password=''
    while True:    
        while True:
            nickname=input('Введите логин(никнейм, только латинские буквы, цифры и знак подчеркивания):\n >>> ')
            if not re.fullmatch(r'[a-zA-Z0-9_]{1,50}', nickname):
                print("Использованы некоректные символы или превышен лимит символов(50). Введите корректное имя пользователя")
                continue
            else: break
        while True:
            password=input('Введите пароль >>> ')
            break
        global user
        user=User(nickname,password, 0)
        if not user.check_user():
            while True:
                print('Данные логин/пароль не совпадают. Пожалуйста, ведите повторно правильные данные - 1\nИли зарегестрируйтесь - 2')
                try:
                    choose=int(input("Ваш выбор >>> "))
                    if choose == 2:
                        sing_in()
                        sys.exit()
                    elif choose == 1:
                        break
                    else:
                        print("Пожалуйста, введите коректное число.")
                except:
                    print("Пожалуйста, введите коректное число.")

        else: break
    print("Вы успешно вошли в учетную запись!\n")
    contact_menu()
    
def sing_in():
    '''Singing in in chat'''
    nickname=''
    password=''
    while True:
        while True:
            nickname=input('Введите логин(никнейм, только латинские буквы, цифры и знак подчеркивания):\n >>> ')
            if not re.fullmatch(r'[a-zA-Z0-9_]{1,50}', nickname):
                print("Использованы некоректные символы или превышен лимит символов(50). Введите корректное имя пользователя")
                continue
            else: break
        while True:
            password=input("Введите пароль >>> ")
            confirm_password=input("Подтвердите пароль >>> ")
            if password == confirm_password:
                break
            else:
                print('Пароли не совпадают. Пожалуйста, введите пароли заново.')
        global user
        user = User(nickname, password, datetime.now().timestamp())
        if not user.save_new_user():
            print('Ошибка регистрации. Данное имя пользователя уже занято. Введите другое')
        else:
            break
    print("Вы успешно зарегестрировались!")
    contact_menu()
    
def contact_menu():
    '''Allows user to choose a contact or exit from chat'''
    menu=0
    exit=False
    global contacts
    contacts=user.get_contacts()
    contacts.remove(user.nickname)
    while True:
        print('Меню контактов\n')
        for i in range(len(contacts)):
            print(f"{i+1} - {contacts[i]}")
        print('e - Выход')
        try:
            choose=(input('Ваш выбор >>> '))
            if choose.lower() == 'e':
    
                exit=True
                break
            try:
                choose=int(choose)
                if choose in range(1, len(contacts)+1):
                    menu=choose-1
                    break
                else:
                    print('Ошибка ввода. Введите правильное число')
            except Exception as e:
                print(f'Ошибка ввода {e}. Введите правильное число')
        except Exception as e:
                print(f'Ошибка ввода {e}. Введите правильное число')        
    
    if exit:
        sys.exit()
    chat_room_menu(contacts[menu])


def chat_room_menu(current_user):
    '''Allows user to refresh messages, write message or go back to contact menu'''
    messages=user.get_message_history(current_user)
    print("\nИстория сообщений:")
    for message in messages:
        print(message.to_str())
    
    while True:
        print('\n')
        print('''Меню: 
        1 - Обновить историю сообщений
        2 - Написать сообщение
        3 - Вернуться в список контактов
        4 - Показать всю историю сообщений
        5 - Выйти из чата''')
        try:
            choose=int(input('Ваш выбор >>> '))
            if choose == 5:
                break
            elif choose == 4:
                print("\nИстория сообщений:")
                for message in messages:
                    print(message.to_str())
            elif choose == 3:
                messages=[]
                contact_menu()
            elif choose == 2:
                try:
                    text=input('\nВведите ваше сообщение >>>')
                    message=Message(user.nickname, current_user, text, datetime.now().timestamp())
                    if user.send_message(message):
                        print("Сообщение успешно доставлено!\n")
                        messages.append(message)
                    else:
                        print('Во время отправки сообщения произошла ошибка. Пожалуйста, попробуйте позже')
                except Exception as e:
                    print(f"Произошла ошибка {e}. Повторите позже")
            elif choose == 1:
                new_messages=user.check_new_message(messages[-1])
                if new_messages != []:
                    print("\nNew massage(s): ")
                    for mes in new_messages:
                        print(mes.to_str())
                    print()
                    messages+=new_messages
                else:
                    print("\nNo new messages")
            else:
                print("Ошибка ввода. Пожалуйста, введите конкретное число")
        except:
            print("Ошибка ввода. Пожалуйста, введите конкретное число")


def main():
    '''Main function that runs programm'''
    first_menu()


if __name__ == "__main__":
    main()