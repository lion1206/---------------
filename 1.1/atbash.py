def prepare_text(text):
    # Замена специальных символов
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')
    return text

def format_output(text):
    # Добавляем пробел после каждого 5-го символа
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

def atbash_encrypt(text):
    # Используем один алфавит для обоих направлений
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    reversed_alphabet = alphabet[::-1]
    
    result = ""
    text = text.upper()
    
    for char in text:
        if char in alphabet:
            index = alphabet.find(char)
            result += reversed_alphabet[index]
        else:
            result += char
    return result

def atbash_decrypt(text):
    # Используем тот же алфавит для расшифровки
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    reversed_alphabet = alphabet[::-1]
    
    result = ""
    text = text.upper()
    
    for char in text:
        if char in reversed_alphabet:
            index = reversed_alphabet.find(char)
            result += alphabet[index]
        else:
            result += char
    return result

def process_large_text(text, encrypt_func):
    # Обработка больших текстов порциями
    result = ""
    chunk_size = 1000
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        processed_chunk = encrypt_func(chunk)
        result += format_output(processed_chunk) + " "
    return result.strip()

def main():
    print("\nВыберите:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Выход")
    
    choice = input("Ваш выбор (от 1 до 3): ")
    
    if choice == '3':
        print("Программа завершена")
        return 0
    
    if choice in ['1', '2']:
        if choice == '1':
            # Шифрование
            text = input("Введите текст: ")
            prepared_text = prepare_text(text)
            result = process_large_text(prepared_text, atbash_encrypt)
            print("\nИсходный текст:")
            print(text)
            print("\nЗашифрованный текст:")
            print(result)
        
        elif choice == '2':
            # Расшифрование
            text = input("Введите зашифрованный текст: ")
            prepared_text = prepare_text(text)
            result = process_large_text(prepared_text, atbash_decrypt)
            print("\nЗашифрованный текст:")
            print(text)
            print("\nРасшифрованный текст:")
            print(result)

if __name__ == "__main__":
    main()
