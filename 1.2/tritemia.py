import re


# Подготовка текста (замена символов и удаление пробелов)
def prepare_text(text):
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')
    return text.upper()

# Форматирование вывода (группировка по 5 символов)
def format_output(text):
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

# Создание таблицы Тритемия
def create_table(alphabet):
    table = []
    for i in range(len(alphabet)):
        row = alphabet[i:] + alphabet[:i]
        table.append(row)
    return table

# Шифрование текста с использованием таблицы Тритемия
def tritemius_encrypt(text):
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    table = create_table(alphabet)
    result = ""
    text = text.upper()

    for i, char in enumerate(text):
        if char in alphabet:
            row = i % len(alphabet)  # Номер строки в таблице соответствует позиции символа
            col = alphabet.index(char)
            result += table[row][col]
        else:
            result += char
    return format_output(result)

# Расшифрование текста с использованием таблицы Тритемия
def tritemius_decrypt(text):
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    table = create_table(alphabet)
    result = ""
    text = text.upper()

    for i, char in enumerate(text):
        if char in alphabet:
            row = i % len(alphabet)  # Номер строки в таблице соответствует позиции символа
            col = table[row].index(char)
            result += alphabet[col]
        else:
            result += char
    return format_output(result)


while True:
    print("\nВыберите:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Выход")

    choice = input("Ваш выбор от (1 до 3): ")

    if choice == '3':
        print("Программа завершена")
        break

    if choice in ['1', '2']:
        if choice == '1':
            # Шифрование
            text = prepare_text(input("Введите текст:"))
            if text:
                result = tritemius_encrypt(text)
                print("\nИсходный текст:")
                print(text)
                print("\nЗашифрованный текст:")
                print(result)

        else:
            # Расшифрование
            text = prepare_text(input("Введите текст:"))
            if text:
                result = tritemius_decrypt(text)
                print("\nЗашифрованный текст:")
                print(text)
                print("\nРасшифрованный текст:")
                print(result)
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3")

