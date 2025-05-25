import np

def prepare_text(text):
    if text is None:
        return ""
    text = text.lower()
    text = text.replace(' ', '')  # Удаляем пробелы
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace('\n', '')
    return text

def rotate_grille(grille):
    """Поворот решетки на 180 градусов по часовой стрелке"""
    return np.rot90(grille, 2)

def mirror_grille(grille):
    """Отзеркаливание решетки по горизонтали"""
    return np.fliplr(grille)

def count_holes(grille):
    """Подсчет количества отверстий в решетке"""
    return np.sum(grille == 0)

def encrypt(text, grille):
    if not text:
        print("Ошибка: пустой текст")
        return None
        
    rows, cols = grille.shape
    text = prepare_text(text)
    
    # Дополняем текст символами 'ъ' до нужной длины
    holes_count = count_holes(grille) * 4  # общее количество отверстий во всех положениях
    if len(text) > holes_count:
        print("Ошибка: текст слишком длинный для данной решетки")
        return None
    while len(text) < holes_count:
        text += 'ъ'
    
    # Создаем пустую матрицу
    message_matrix = [['ъ' for _ in range(cols)] for _ in range(rows)]
    text_pos = 0
    
    # Заполняем матрицу через все четыре положения решетки
    current_grille = grille.copy()
    for rotation in range(4):
        print(f"\nПоворот решетки на {rotation * 180} градусов:")
        print("Решетка:")
        print(current_grille)
        print("Матрица с текстом до заполнения:")
        print_matrix(message_matrix)
        
        for i in range(rows):
            for j in range(cols):
                if current_grille[i][j] == 0:
                    message_matrix[i][j] = text[text_pos]
                    text_pos += 1
        
        print("Матрица с текстом после заполнения:")
        print_matrix(message_matrix)
        
        # Поворачиваем решетку на 180 градусов
        if rotation % 2 == 1:
            current_grille = rotate_grille(current_grille)
        
        # Отзеркаливаем решетку
        if rotation % 2 == 0:
            current_grille = mirror_grille(current_grille)
    
    # Собираем зашифрованный текст
    encrypted = ''
    for i in range(rows):
        for j in range(cols):
            encrypted += message_matrix[i][j]
    
    return encrypted

def decrypt(encrypted_text, grille):
    if not encrypted_text:
        print("Ошибка: пустой зашифрованный текст")
        return None
        
    rows, cols = grille.shape
    if len(encrypted_text) != rows * cols:
        print("Ошибка: длина зашифрованного текста не соответствует размеру решетки")
        return None
    
    # Преобразуем зашифрованный текст в матрицу
    message_matrix = []
    for i in range(0, len(encrypted_text), cols):
        message_matrix.append(list(encrypted_text[i:i+cols]))
    
    decrypted = ''
    current_grille = grille.copy()
    
    # Читаем текст через отверстия в четырех положениях
    for rotation in range(4):
        print(f"\nПоворот решетки на {rotation * 180} градусов:")
        print("Решетка:")
        print(current_grille)
        print("Матрица с текстом:")
        print_matrix(message_matrix)
        
        for i in range(rows):
            for j in range(cols): 
                    if current_grille[i][j] == 0:
                        decrypted += message_matrix[i][j]
        
        # Поворачиваем решетку на 180 градусов
        current_grille = rotate_grille(current_grille)
        
        # Отзеркаливаем решетку
        if rotation % 2 == 0:
            current_grille = mirror_grille(current_grille)
    
    # Удаляем символы 'ъ' из расшифрованного текста
    decrypted = decrypted.rstrip('ъ')
    
    return decrypted

def print_matrix(matrix):
    """Вспомогательная функция для вывода матрицы"""
    for row in matrix:
        print(' '.join(row))

def main():
    # Определяем решетку
    grille = np.array([
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 0]
    ])

    while True:
        print("\nВыберите действие:")
        print("1. Зашифровать текст из файла")
        print("2. Расшифровать текст из файла")
        print("3. Выход")
        
        choice = input("Ваш выбор (1-3): ")
        
        if choice == '3':
            print("Программа завершена")
            break
            
        if choice == '1':
            text = input("Введите текст: ")
            if text:
                encrypted = encrypt(text, grille)
                if encrypted:
                    print("\nИсходный текст:")
                    print(text)
                    print("\nЗашифрованный текст:")
                    print(encrypted)
                    # Сохраняем зашифрованный текст в файл
                    with open("1.4/untest.txt", 'w', encoding='utf-8') as f:
                        f.write(encrypted)
                
        elif choice == '2':
            text = input("Введите зашифрованный текст: ")
            if text:
                decrypted = decrypt(text, grille)
                if decrypted:
                    print("\nЗашифрованный текст:")
                    print(text)
                    print("\nРасшифрованный текст:")
                    print(decrypted)
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3")

if __name__ == "__main__":
    main()

    # исправить чтобы заполнялось разными пустышками 