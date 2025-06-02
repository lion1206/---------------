# Создаем квадрат Полибия для русского алфавита (без Ё)
polybius_square = [
    ['А', 'Б', 'В', 'Г', 'Д', 'Е'],
    ['Ж', 'З', 'И', 'Й', 'К', 'Л'],
    ['М', 'Н', 'О', 'П', 'Р', 'С'],
    ['Т', 'У', 'Ф', 'Х', 'Ц', 'Ч'],
    ['Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э'],
    ['Ю', 'Я', ' ', '!', '?', '-']  # Добавляем символы для заполнения
]

# Функция для подготовки текста
def prepare_text(text):
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')  # Удаляем пробелы
    return text

# Функция для форматирования вывода
def format_output(text):
    # Добавляем пробел после каждого 5-го символа
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

# Функция для шифрования текста с использованием квадрата Полибия
def polybius_encrypt(text):
    encrypted_text = ""
    for char in text.upper():
        found = False
        for row in range(6):
            for col in range(6):
                if polybius_square[row][col] == char:
                    encrypted_text += str(row + 1) + str(col + 1)
                    found = True
                    break
            if found:
                break
        if not found:
            encrypted_text += "00"  # Если символ не найден, заменяем на "00"
    return encrypted_text

# Функция для расшифрования текста с использованием квадрата Полибия
def polybius_decrypt(text):
    decrypted_text = ""
    text = text.replace(' ', '').replace('\n', '')  # Убираем пробелы и символы новой строки перед расшифровкой
    for i in range(0, len(text), 2):
        try:
            row = int(text[i]) - 1
            col = int(text[i + 1]) - 1
            if row >= 0 and row < 6 and col >= 0 and col < 6:
                decrypted_text += polybius_square[row][col]
            else:
                decrypted_text += "?"  # Если координаты некорректны, заменяем на "?"
        except Exception as e:
            decrypted_text += "?"  # Обработка ошибок при конвертации
    return decrypted_text

# Функция для обработки больших текстов
def process_large_text(text, encrypt_func):
    result = ""
    chunk_size = 1000
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        processed_chunk = encrypt_func(chunk)
        result += format_output(processed_chunk) + " "
    return result.strip()

while True:
    print("\nВыберите:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Выход")

    choice = input("Ваш выбор (от 1 до 3): ")

    if choice == '3':
        print("Программа завершена")
        break

    if choice in ['1', '2']:
        if choice == '1':
            # Шифрование
            text = input("Введите текст: ")
            prepared_text = prepare_text(text)
            result = process_large_text(prepared_text, polybius_encrypt)
            print("\nИсходный текст:")
            print(text)
            print("\nЗашифрованный текст:")
            print(result)

        else:
            # Расшифрование
            text = input("Введите зашифрованный текст: ")
            prepared_text = prepare_text(text)
            result = process_large_text(prepared_text, polybius_decrypt)
            print("\nЗашифрованный текст:")
            print(text)
            print("\nРасшифрованный текст:")
            print(result)

    else:
        print("Неверный выбор. Пожалуйста, выберите от 1 до 3.")