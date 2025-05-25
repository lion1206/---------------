def cols_rows(text_length, key):
    # Вычисляем количество столбцов на основе длины ключа
    cols = len(key)
    rows = (text_length + cols - 1) // cols  # Вычисляем необходимое количество строк
    return rows, cols

def print_matrix(matrix, title="Матрица"):
    print(f"{title}:")
    for row in matrix:
        print(" ".join(row))
    print()

def is_valid_key(key):
    # Проверяем, что в ключе нет буквы 'ё'
    if 'Ё' in key or 'ё' in key:
        return False, "В ключе не должно быть буквы 'ё'."
    return True, ""

def preprocess_text(text):
    # Заменяем точки и запятые
    text = text.replace(".", "тчк").replace(",", "зпт")
    return text

def encrypt_route_transposition(text, key):
    # Удаляем пробелы и приводим текст к верхнему регистру
    text = text.replace(" ", "").upper().replace("Ё", "Е")
    text_length = len(text)

    # Вычисляем размер таблицы
    rows, cols = cols_rows(text_length, key)

    # Дополняем текст пробелами, если его длина не кратна размеру таблицы
    padding_length = rows * cols - text_length
    padded_text = text + ' ' * padding_length

    # Создаем матрицу и заполняем её текстом
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0
    for row in range(rows):
            
        for col in range(cols):
            matrix[row][col] = padded_text[index]
            index += 1


    # Выводим промежуточную матрицу
    print_matrix(matrix, "Матрица после записи текста")

    # Определяем порядок столбцов на основе ключа
    key_order = sorted(range(cols), key=lambda k: key[k])

    # Читаем столбцы в порядке, заданном ключом
    encrypted_text = ''
    for col in key_order:
        for row in range(rows):
            encrypted_text += matrix[row][col]

    # Удаляем пробелы из зашифрованного текста
    encrypted_text_no_spaces = encrypted_text.replace(" ", "")

    return encrypted_text, encrypted_text_no_spaces

def decrypt_route_transposition(encrypted_text_with_spaces, key):
    text_length = len(encrypted_text_with_spaces)

    # Вычисляем размер таблицы
    rows, cols = cols_rows(text_length, key)

    # Определяем порядок столбцов на основе ключа
    key_order = sorted(range(cols), key=lambda k: key[k])

    # Создаем пустую матрицу
    matrix = [['' for _ in range(cols)] for _ in range(rows)]

    # Заполняем матрицу зашифрованным текстом в порядке, заданном ключом
    index = 0
    for col in key_order:
        for row in range(rows):
            matrix[row][col] = encrypted_text_with_spaces[index]
            index += 1

    # Выводим промежуточную матрицу
    print_matrix(matrix, "Матрица после записи зашифрованного текста")

    # Читаем матрицу построчно, чтобы получить расшифрованный текст
    decrypted_text = ''
    for row in range(rows):
        for col in range(cols):
            decrypted_text += matrix[row][col]

    return decrypted_text

while True:
    print("Выберите операцию:")
    print("1. Зашифровать")
    print("2. Расшифровать")
    print("3. Выйти")
    choice = input("Введите номер операции: ")

    if choice == '1':
        text = input("Введите текст для шифрования: ")
        text = preprocess_text(text)
        key = input("Введите ключ: ").upper()
        valid, error = is_valid_key(key)
        if not valid:
            print("Ошибка:", error)
            continue
        encrypted_text, encrypted_text_no_spaces = encrypt_route_transposition(text, key)
        print("Зашифрованный текст:", encrypted_text_no_spaces)
        # Сохраняем зашифрованный текст с пробелами для последующей расшифровки
        encrypted_text_with_spaces = encrypted_text
    elif choice == '2':
        if 'encrypted_text_with_spaces' not in locals():
            print("Сначала зашифруйте текст.")
            continue
        key = input("Введите ключ: ").upper()
        valid, error = is_valid_key(key)
        if not valid:
            print("Ошибка:", error)
            continue
        decrypted_text = decrypt_route_transposition(encrypted_text_with_spaces, key)
        print("Расшифрованный текст:", decrypted_text)
    elif choice == '3':
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
