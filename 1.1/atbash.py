def prepare_text(text):
    
    text = text.replace(',', 'зпт')
    text = text.replace('.', 'тчк')
    text = text.replace(' ', '')

    return text

def format_output(text):
    # Добавляем пробел после каждого 5-го символа
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])



def atbash_encrypt(text):
    
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
    result = format_output(result)
    
    return result

def atbash_decrypt(text):
    
    return atbash_encrypt(text)


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
        if choice == '1':
            
            # Шифрование
            text = prepare_text(input("Введите текст: "))
            result = atbash_encrypt(text)
            print("\nИсходный текст:")
            print(text)
            print("\nЗашифрованный текст:")
            print(result)
            
        elif choice == '2':
            # Расшифрование
            text = prepare_text(input("Введите зашифрованный текст: "))
            result = atbash_decrypt(text)
            print("\nЗашифрованный текст:")
            print(result)
            print("\nРасшифрованный текст:")
            print(text)
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3")

