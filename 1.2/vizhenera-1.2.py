def read_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return None

def prepare_text(text):
    # Заменяем запятые и точки
    text = text.replace(',', 'зпт').replace('.', 'тчк')
    # Убираем пробелы
    text = text.replace(' ', '')
    # Приводим текст к верхнему регистру
    text = text.upper()
    return text

def restore_text(text):
    # Восстанавливаем запятые и точки
    text = text.replace('зпт', ',').replace('тчк', '.')
    return text

def generate_self_key(text, initial_key):
    """
    Генерация самоключа на основе начального ключа и текста.
    """
    key = initial_key.upper()
    for char in text:
        key += char
    return key

def vigenere_encrypt(text, key):
    encrypted_text = ""
    for i, char in enumerate(text):
        if char in alphabet:
            # Вычисляем сдвиг на основе символа ключа
            key_char = key[i % len(key)]
            key_index = alphabet.index(key_char)
            char_index = alphabet.index(char)
            # Шифруем символ
            encrypted_char = alphabet[(char_index + key_index) % len(alphabet)]
            encrypted_text += encrypted_char
        else:
            # Если символ не в алфавите, оставляем его как есть
            encrypted_text += char
    return encrypted_text

def vigenere_decrypt(encrypted_text, initial_key):
    decrypted_text = ""
    key = initial_key.upper()  # Начинаем с начального ключа
    for i, char in enumerate(encrypted_text):
        if char in alphabet:
            # Вычисляем сдвиг на основе символа ключа
            key_char = key[i % len(key)]
            key_index = alphabet.index(key_char)
            char_index = alphabet.index(char)
            # Расшифровываем символ
            decrypted_char = alphabet[(char_index - key_index) % len(alphabet)]
            decrypted_text += decrypted_char
            # Обновляем ключ для следующего символа
            key += decrypted_char
        else:
            # Если символ не в алфавите, оставляем его как есть
            decrypted_text += char
    return decrypted_text

def is_valid_key(key):
    """
    Проверяет, что ключ состоит ровно из одной буквы.
    """
    return len(key) == 1 and key.upper() in alphabet

def main():
    global alphabet
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"  # Полный русский алфавит
    
    while True:
        print("\nВыберите действие:")
        print("1. Зашифровать текст из файла")
        print("2. Расшифровать текст из файла")
        print("3. Выход")
        
        choice = input("Ваш выбор (1-3): ")
        
        if choice == '3':
            print("Программа завершена")
            break
        
        if choice in ['1', '2']:
            while True:
                initial_key = input("Введите начальный ключ (одна буква): ")
                if is_valid_key(initial_key):
                    break
                else:
                    print("Ошибка: ключ должен состоять ровно из одной буквы русского алфавита.")
            
            initial_key = prepare_text(initial_key)  # Подготавливаем ключ
            
            if choice == '1':
                text = read_from_file("1.2/fraza.txt")
                if text:
                    prepared_text = prepare_text(text)
                    # Генерация самоключа
                    self_key = generate_self_key(prepared_text, initial_key)
                    encrypted_text = vigenere_encrypt(prepared_text, self_key)
                    print("\nИсходный текст:")
                    print(text)
                    print("\nСамоключ:")
                    print(self_key)
                    print("\nЗашифрованный текст:")
                    print(encrypted_text)
            
            else:
                encrypted_text = read_from_file("1.2/nofraza.txt")
                if encrypted_text:
                    # Расшифровка с использованием начального ключа
                    decrypted_text = vigenere_decrypt(encrypted_text, initial_key)
                    # Восстанавливаем исходный текст (заменяем "зпт" и "тчк" обратно)
                    restored_text = restore_text(decrypted_text)
                    print("\nЗашифрованный текст:")
                    print(encrypted_text)
                    print("\nРасшифрованный текст:")
                    print(restored_text)
        else:
            print("Выберите 1, 2 или 3")

if __name__ == "__main__":
    main()