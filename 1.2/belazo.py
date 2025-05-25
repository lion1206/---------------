import re

def is_valid_key(key):
    # Регулярное выражение для проверки строки
    pattern = r'^[а-яА-Я]+$'
    return bool(re.match(pattern, key))

def prepare_text(text):
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')
    return text.upper()

def format_output(text):
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

def create_matrix():
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    matrix = []
    for i in range(len(alphabet)):
        row = alphabet[i:] + alphabet[:i]
        matrix.append(row)
    return matrix, alphabet

def belaso_encrypt(text, key):
    matrix, alphabet = create_matrix()
    result = ""
    text = text.upper()
    key = key.upper()
    key_length = len(key)

    for i in range(len(text)):
        if text[i] in alphabet:
            row = alphabet.index(key[i % key_length])
            col = alphabet.index(text[i])
            result += matrix[row][col]
        else:
            result += text[i]

    return format_output(result)

def belaso_decrypt(text, key):
    matrix, alphabet = create_matrix()
    result = ""
    text = text.upper()
    key = key.upper()
    key_length = len(key)

    for i in range(len(text)):
        if text[i] in alphabet:
            row = alphabet.index(key[i % key_length])
            row_alphabet = matrix[row]
            col = row_alphabet.index(text[i])
            result += alphabet[col]
        else:
            result += text[i]

    return format_output(result)


while True:
    print("\nВыберите:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Выход")

    choice = input("Ваш выбор от 1 до 3): ")

    if choice == '3':
        print("Программа завершена")
        break

    if choice in ['1', '2']:
        key = input("Введите ключ: ").upper()

        if not key:
            print("Ошибка: ключ не может быть пустым")
            continue

        if not is_valid_key(key):
            print("Ошибка: ключ должен содержать только буквы русского алфавита (за исключением 'ё') и не содержать цифр или знаков препинания")
            continue

        if choice == '1':
            # Шифрование
            text = prepare_text(input("Введите текст:"))
            if text:
                result = belaso_encrypt(text, key)
                print("\nИсходный текст:")
                print(text)
                print("\nЗашифрованный текст:")
                print(result)

        else:
            # Расшифрование
            text = prepare_text(input("Введите текст:"))
            if text:
                result = belaso_decrypt(text, key)
                print("\nРасшифрованный текст:")
                print(text)
                print("\nЗашифрованный текст:")
                print(result)
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3")

