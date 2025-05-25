def prepare_text(text):
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')  # Удаляем пробелы
    return text

def format_output(text):
    # Добавляем пробел после каждого 5-го символа
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

def caesar_cipher(text, shift, decrypt=False):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    result = []

    for char in text:
        if char.lower() in alphabet:
            is_upper = char.isupper()
            index = alphabet.index(char.lower())
            if decrypt:
                new_index = (index - shift) % len(alphabet)
            else:
                new_index = (index + shift) % len(alphabet)
            new_char = alphabet[new_index]
            if is_upper:
                new_char = new_char.upper()
            result.append(new_char)
        else:
            result.append(char)

    return ''.join(result)

def caesar_encrypt(text, shift):
    encrypted_text = caesar_cipher(text, shift)
    return format_output(encrypted_text).lower()  # Начинаем с маленькой буквы

def caesar_decrypt(text, shift):
    # Убираем пробелы перед расшифровкой
    text = text.replace(' ', '')
    return caesar_cipher(text, shift, decrypt=True)

while True:
    print("\nВыберите:")
    print("1. Зашифровать текст из файла")
    print("2. Расшифровать текст из файла")
    print("3. Выход")

    choice = input("Ваш выбор (от 1 до 3): ")

    if choice == '3':
        print("Программа завершена")
        break

    if choice in ['1', '2']:
        shift = int(input("Введите сдвиг для шифра Цезаря: "))
        if not (1 <= shift <= 31):
            print('Неверный параметр, введите сдвиг от 1 до 31')
            continue

        if choice == '1':
            # Шифрование
            text = prepare_text(input("Введите текст: "))
            if text:
                result = caesar_encrypt(text, shift)
                print("\nИсходный текст:")
                print(text)
                print("\nЗашифрованный текст:")
                print(result)

        else:
            # Расшифрование
            text = prepare_text(input("Введите зашифрованный текст: "))
            if text:
                result = caesar_decrypt(text, shift)
                print("\nЗашифрованный текст:")
                print(text)
                print("\nРасшифрованный текст:")
                print(result)
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3")

