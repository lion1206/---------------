import numpy as np
import random

def prepare_text(text):
    text = text.lower().replace(' ', '').replace(',', 'зпт').replace('.', 'тчк').replace('\n', '')
    return text

def rotate_grille(grille):
    return np.rot90(grille, 2)

def mirror_grille(grille):
    return np.fliplr(grille)

def count_holes(grille):
    return np.sum(grille == 0)

def generate_padding_symbols(n):
    pool = list("абвгдежзиклмнопрстуфхцчшщыьэюя")  # Ё, Й, Ъ исключены
    return ''.join(random.choice(pool) for _ in range(n))

def encrypt(block_text, grille):
    rows, cols = grille.shape
    holes_count = count_holes(grille) * 4

    # Дополняем, если нужно
    if len(block_text) < holes_count:
        padding = generate_padding_symbols(holes_count - len(block_text))
        block_text += padding
        print(f"Добавлены символы для дополнения: {padding}")

    message_matrix = [['' for _ in range(cols)] for _ in range(rows)]
    text_pos = 0
    current_grille = grille.copy()

    for rotation in range(4):
        for i in range(rows):
            for j in range(cols):
                if current_grille[i][j] == 0:
                    message_matrix[i][j] = block_text[text_pos]
                    text_pos += 1
        current_grille = rotate_grille(current_grille)
        if rotation % 2 == 0:
            current_grille = mirror_grille(current_grille)

    return ''.join(''.join(row) for row in message_matrix)

def decrypt(block_text, grille):
    rows, cols = grille.shape
    message_matrix = [list(block_text[i:i+cols]) for i in range(0, len(block_text), cols)]
    decrypted = ''
    current_grille = grille.copy()

    for rotation in range(4):
        for i in range(rows):
            for j in range(cols):
                if current_grille[i][j] == 0:
                    decrypted += message_matrix[i][j]
        current_grille = rotate_grille(current_grille)
        if rotation % 2 == 0:
            current_grille = mirror_grille(current_grille)

    return decrypted

def encrypt_long_text(text, grille):
    text = prepare_text(text)
    holes_count = count_holes(grille) * 4
    block_length = holes_count
    blocks = [text[i:i+block_length] for i in range(0, len(text), block_length)]
    encrypted_blocks = []

    for block in blocks:
        encrypted = encrypt(block, grille)
        if encrypted:
            encrypted_blocks.append(encrypted)

    return ''.join(encrypted_blocks)

def decrypt_long_text(encrypted_text, grille):
    rows, cols = grille.shape
    block_length = rows * cols
    blocks = [encrypted_text[i:i+block_length] for i in range(0, len(encrypted_text), block_length)]
    decrypted_text = ''

    for block in blocks:
        decrypted = decrypt(block, grille)
        if decrypted:
            decrypted_text += decrypted

    return decrypted_text

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(row))

def main():
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
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Выход")

        choice = input("Ваш выбор: ")

        if choice == '3':
            print("Программа завершена")
            break

        elif choice == '1':
            text = input("Введите текст для шифрования: ")
            encrypted = encrypt_long_text(text, grille)
            if encrypted:
                print("\nЗашифрованный текст:")
                print(encrypted)

        elif choice == '2':
            encrypted = input("Введите зашифрованный текст: ")
            decrypted = decrypt_long_text(encrypted, grille)
            if decrypted:
                print("\nРасшифрованный текст:")
                print(decrypted)

        else:
            print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

if __name__ == "__main__":
    main()
