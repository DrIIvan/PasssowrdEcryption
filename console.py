from crypto_functions import AES256_encryption, add_bytes, AES256_decryption, clear_added_bytes, get_random_key
from db_functions import add_account, get_account, delete_account, update_account
import os

# -----------------------------------------------------------------------------------------
# Создание переменных и констант.----------------------------------------------------------

# Информация о командах.
info = {
    "add": """
Команда имеет аргумент количества добавленных аккаунтов
и вносит их в память текущей сессии. 
""",
    "stop": """
Команда имеет аргумент режима работы('s', 'q', 'qs'). 
's' - сохранение без выхода
'q' - выход без сохранения
'qs' - выход и сохранение 
""",
    "help": """
Команда выводит список команд и их описание. 
""",
    "get": """
Команда выводит список паролей подходящих по поисковому ключу.
Если в качестве ключа ввести 'NONE', то будет выведен список всех паролей.
""",
    "remove": """
Команда удаляет запись из базы данных по названию аккаунта.
Если в качестве названия ввести 'DELETE_ALL', то будет очищена вся база данных.
""",
    "update": """
Команда перезаписывает все пароли с новый ключом шифрования.
""",
}

# Константа размера ключа шифрования.
DATABASE_NAME = "passwords"
KEY_SIZE = 32

# Переменная для записи всех новых аккаунтов в текущей сессии.
new_accounts = []

# Получаем ключ шифрования из файла.
with open("./data_base/key.txt", "rb") as f:
    KEY = f.read()

# Выводим отладочную информацию.
# print(f"Размер ключа - {KEY_SIZE}")
# print(f"Ключ - {KEY}")

# -----------------------------------------------------------------------------------------
# Функции команд.--------------------------------------------------------------------------


# Команда добавления записей в базу данных.
def add():
    number = input("--> add | Введите кол-во добавлений: ")
    try:
        for i in range(int(number)):
            print(f"--> add {i+1}/{number} |", end=" ")

            current_account = input("Введите название и пароль через '/': ").split("/")
            bytes_like_password = add_bytes(current_account[1], KEY_SIZE)
            new_accounts.append([current_account[0], AES256_encryption(bytes_like_password.encode(), KEY)])
    except IndexError or ValueError:
        print("Неправильный синтаксис при использовании команды 'add'.")


# Команда остановки и сохранения записей и текущей сессии.
def stop():
    mode = input("--> stop | Введите режим работы('q', 's', 'qs'): ")

    if mode == "qs":
        for account in new_accounts:
            add_account(account[0], account[1], DATABASE_NAME)
        print(f"--> stop(res) | Данные в текущей сессии успешно сохранены в базу данных")
        return "quit"
    elif mode == "s":
        for account in new_accounts:
            add_account(account[0], account[1], DATABASE_NAME)
        print(f"--> stop(res) | Данные в текущей сессии успешно сохранены в базу данных")
    elif mode == "q":
        return "quit"


# Команда вывода информации о доступных командах.
def help():
    for command in info:
        print(f"{command}:{info[command]}")


# Вывод аккаунтов по запросу из базы данных.
def get():
    mode = input("--> get | Введите ключ поиска: ")
    res = get_account(mode, DATABASE_NAME)

    for account in res:
        decoded_password = clear_added_bytes(AES256_decryption(account[1], KEY))
        print(f"{account[0]} - {decoded_password}")


# Удаление аккаунтов из базы данных.
def remove():
    service = input("--> remove | Введите названия аккаунта: ")

    if service == "DELETE_ALL":
        confirm = input("--> remove | Вы уверены что хотите полностью очистить базу данных с паролями(Y/N)? ").replace(" ", "")
        if confirm == "Y":
            delete_account(service, DATABASE_NAME)
            print(f"--> remove(res) | База данных с паролями полностью очищена.")
    else:
        delete_account(service, DATABASE_NAME)
        print(f"--> remove(res) | Аккаунт '{service}' успешно удалены из базы данных")


# Обновление всех записей под новый ключ шифрования.
def update():
    new_key = get_random_key(32)

    res = get_account("NONE", DATABASE_NAME)

    for service in res:
        decode = AES256_decryption(service[1], KEY)
        encode = AES256_encryption(decode.encode(), new_key)
        update_account(service[0], encode, DATABASE_NAME)

    with open("./data_base/key.txt", "wb") as bin_file:
        bin_file.write(new_key)
    print("--> update(res) | Пароли и ключ шифрования успешно обновлены")
    return "quit"


def clear():
    os.system("cls")


# -----------------------------------------------------------------------------------------
# Функция консоли(обработчика команд).-----------------------------------------------------

def console():
    # Функция для обработки команд в консоли.
    while True:
        # Вывод знака готовности к принятию команд.
        print("-->", end=" ")

        # Ожидаем команду от пользователя.
        command = input()
        command = command.replace(" ", "")

        # Определяем какая команда введена.
        if command == "add":
            add()
        elif command == "stop":
            if stop() == "quit":
                break
        elif command == "get":
            get()
        elif command == "remove":
            remove()
        elif command == "update":
            if update() == "quit":
                break
        elif command == "clear":
            clear()
        elif command == "help":
            help()
        elif command != "":
            print(f"'{command}' не является встроенной командой. Для просмотра списка всех доступных команд введите 'help'")


console()
