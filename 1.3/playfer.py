def prepare_text(text):
    
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')
    
    text = text.upper()
    text = text.replace('Ё', 'Е')
    text = text.replace('Й', 'И')
    text = text.replace('Ъ', 'Ь')
    return text

def split_into_bigrams(text):
    result = []
    i = 0
    while i < len(text):
        if i == len(text) - 1:  
            result.append(text[i] + 'Ф')
            break
        elif text[i] == text[i + 1]:  
            result.append(text[i] + 'Ф')
            i += 1
        else:
            result.append(text[i:i+2])
            i += 2
    return result

def format_output(text):
    return ' '.join(text if isinstance(text, list) else [text[i:i+2] for i in range(0, len(text), 2)])

def create_playfair_matrix(key):
    
    alphabet = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЬЫЭЮЯ"
    key = key.upper()
    key = key.replace('Ё', 'Е').replace('Й', 'И').replace('Ъ', 'Ь')
    
    
    key = ''.join(dict.fromkeys(key))
    
    matrix = []
    used_chars = set()
    
    
    for char in key:
        if char in alphabet and char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    # 5x6
    return [matrix[i:i+6] for i in range(0, 30, 6)]

def find_position(matrix, char):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == char:
                return i, j
    return None

def playfair_encrypt(bigrams, matrix):
    result = []
    for bigram in bigrams:
        a, b = bigram[0], bigram[1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:  # в одной строке
            new_bigram = matrix[row1][(col1 + 1) % 6] + matrix[row2][(col2 + 1) % 6]
        elif col1 == col2:  # в одном столбце
            new_bigram = matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:  # бразуют прямоугольник
            new_bigram = matrix[row1][col2] + matrix[row2][col1]
        result.append(new_bigram)
    
    return result

def playfair_decrypt(bigrams, matrix):
    result = []
    for bigram in bigrams:
        a, b = bigram[0], bigram[1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:  # в одной строке
            new_bigram = matrix[row1][(col1 - 1) % 6] + matrix[row2][(col2 - 1) % 6]
        elif col1 == col2:  # в одном столбце
            new_bigram = matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:  # образуют прямоугольник
            new_bigram = matrix[row1][col2] + matrix[row2][col1]
        result.append(new_bigram)
    
    return result

def check_key(key):
    """
    Проверяет ключ на наличие повторяющихся букв
    Возвращает True, если ключ валидный (нет повторений)
    Возвращает False, если есть повторяющиеся буквы
    """
    # Приводим к верхнему регистру и заменяем специальные буквы
    key = key.upper()
    key = key.replace('Ё', 'Е').replace('Й', 'И').replace('Ъ', 'Ь1')
    
    # Создаем множество символов
    seen_chars = set()
    
    for char in key:
        if char in seen_chars:
            return False
        seen_chars.add(char)
    
    return True


while True:
    print("\nВыберите действие:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Выход")
    
    choice = input("Ваш выбор (от 1 до 3): ")
    
    if choice == '3':
        print("Программа завершена")
        break
    
    if choice in ['1', '2']:
        while True:
            key = input("Введите ключ: ")
            if check_key(key):
                break
            else:
                print("Ошибка: в ключе есть повторяющиеся буквы. Введите другой ключ.")
        
        matrix = create_playfair_matrix(key)
        
        print("\nМатрица:")
        for row in matrix:
            print(row)
        
        
        if choice == '1':
            text = input("Введите текст: ")
            if text:
                prepared_text = prepare_text(text)
                bigrams = split_into_bigrams(prepared_text)
                result = playfair_encrypt(bigrams, matrix)
                print("\nИсходный текст:")
                print(text)
                print("\nтекст в биграммах:")
                print(' '.join(bigrams))
                print("\nЗашифрованный текст:")
                print(' '.join(result))
        
        else:
            text = input("Введите зашифрованный текст: ")
            if text:
                prepared_text = prepare_text(text)
                bigrams = [prepared_text[i:i+2] for i in range(0, len(prepared_text), 2)]
                result = playfair_decrypt(bigrams, matrix)
                print("\nЗашифрованный текст:")
                print(text)
                print("\nРасшифрованный текст:")
                print(' '.join(result))
    else:
        print("выберите 1, 2 или 3")