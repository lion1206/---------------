import math

alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"

def preprocess_text(text):
    """Подготовка текста: верхний регистр, замена знаков препинания"""
    text = text.upper()
    text = text.replace('.', 'ТЧК')
    text = text.replace(',', 'ЗПТ')
    text = text.replace(' ', 'ПРБ')
    text = text.replace('Ё', 'Е')
    # Удаляем символы, не входящие в алфавит
    return ''.join(char for char in text if char in alphabet)

def postprocess_text(text):
    """Восстановление текста после расшифрования"""
    text = text.replace('ЗПТ', ',')
    text = text.replace('ТЧК', '.')
    text = text.replace('ПРБ', ' ')
    return text

def is_prime(n):  
    if n <= 1:  
        return False  
    for i in range(2, int(n**0.5) + 1):  
        if n % i == 0:  
            return False  
    return True  

def is_coprime(x, y):
    return math.gcd(x, y) == 1

def f_d(e, N):
    for i in range(N):
        if e * i % N == 1:
            return i

def fi(n):
    f = n
    if n % 2 == 0:
        while n % 2 == 0:
            n = n // 2
        f = f // 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n = n // i
            f = f // i
            f = f * (i - 1)
        i = i + 2
    if n > 1:
        f = f // n
        f = f * (n - 1)
    return f

def rsa():
    string = input("Введите сообщение: ")
    string = preprocess_text(string)
    
    # Проверка, что в строке есть допустимые символы
    if not string:
        print("Сообщение не содержит символов из алфавита после обработки!")
        return []
    
    while True:
        P = int(input("Введите число P (простое): "))
        if not is_prime(P):
            print("Число должно быть простым")
            continue
        Q = int(input("Введите число Q (простое): "))
        if not is_prime(Q):
            print("Число должно быть простым")
            continue
        N = P * Q
        print(f"P*Q = {N}")
        if N < 32:
            print("P*Q < 32")
            continue
        break

    f = fi(N)
    while True:
        e = int(input(f"Введите е, 1 < e < {f} взаимно простое с {f}: "))
        if e <= 1 or e >= f:
            print(f"e должно быть в интервале (1, {f})")
            continue
        if not is_coprime(f, e):
            print(f"e и φ(N) должны быть взаимно простыми")
            continue
        if f_d(e, f) == e:
            print("e не должно быть равно закрытому ключу, выберите другое значение e: ")
            continue
        break
        
    d = f_d(e, f)
    print(f"Открытый ключ (e={e}, N={N}), Закрытый ключ d={d}")
    
    # Шифрование каждого символа
    fin = []
    for c in string:
        try:
            char_index = alphabet.index(c)
            encrypted_char = pow(char_index, e, N)
            fin.append(encrypted_char)
        except ValueError:
            print(f"Пропущен недопустимый символ: {c}")
    
    return fin

def rsaun(encrypted_list):
    N = int(input("Введите число N: "))
    d = int(input("Введите d: "))
    
    decoded = []
    for val in encrypted_list:
        decrypted_index = pow(val, d, N)
        decoded.append(alphabet[decrypted_index])
    
    decrypted_text = ''.join(decoded)
    return postprocess_text(decrypted_text)

# Основная программа
encrypted_data = []

while True:
    print("\n--- Меню ---")
    print("1. Зашифровать сообщение")
    print("2. Расшифровать сообщение")
    print("3. Выход")
    
    choice = input("Выберите действие: ")
    
    if choice == '1':
        encrypted_data = rsa()
        if encrypted_data:
            print(f"Зашифрованное сообщение: {encrypted_data}")
            
    elif choice == '2':
        if not encrypted_data:
            print("Сначала зашифруйте сообщение или введите данные вручную")
            encrypted_input = input("Введите числа через пробел: ").split()
            try:
                encrypted_data = [int(x) for x in encrypted_input]
            except ValueError:
                print("Ошибка ввода! Используйте только целые числа")
                continue
                
        decrypted_text = rsaun(encrypted_data)
        print(f"Расшифрованное сообщение: {decrypted_text}")
        
    elif choice == '3':
        print("Выход из программы.")
        break
        
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")