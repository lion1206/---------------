import random
import math
import sys

# Расширенная таблица русских символов с гарантированной поддержкой точек и запятых
RUSSIAN_ALPHABET = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя.,"

def char_to_num(char):
    """Преобразует символ в число согласно таблице"""
    # Приводим символ к нижнему регистру перед обработкой
    char_lower = char.lower()
    if char_lower in RUSSIAN_ALPHABET:
        return RUSSIAN_ALPHABET.index(char_lower) + 1
    return char_to_num(' ')  # заменяем на пробел

def num_to_char(num):
    """Преобразует число обратно в символ"""
    if 1 <= num <= len(RUSSIAN_ALPHABET):
        return RUSSIAN_ALPHABET[num - 1]
    return '�'

def phi(n):
    """Вычисляет функцию Эйлера для n"""
    if n == 1:
        return 1
    result = n
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
    if n > 1:
        result -= result // n
    return result

def fracDivided(top, bottom, p):
    """Выполняет деление по модулю p"""
    if bottom % p == 0:
        return 0
    inv = pow(bottom, phi(p) - 1, p)
    return (top * inv) % p

def dotAdding(x1, y1, x2, y2, p, a):
    """Сложение точек на эллиптической кривой"""
    if x1 == 0 and y1 == 0:
        return x2, y2
    if x2 == 0 and y2 == 0:
        return x1, y1
    if x1 == x2 and (y1 + y2) % p == 0:
        return 0, 0

    if x1 != x2:
        gamma = fracDivided(y2 - y1, x2 - x1, p)
    else:
        gamma = fracDivided(3 * x1 ** 2 + a, 2 * y1, p)

    x3 = (gamma ** 2 - x1 - x2) % p
    y3 = (gamma * (x1 - x3) - y1) % p
    return x3, y3

def dotDoubler(x1, y1, p, a):
    """Удвоение точки на эллиптической кривой"""
    if y1 == 0:
        return 0, 0
    gamma = fracDivided(3 * x1 ** 2 + a, 2 * y1, p)
    x3 = (gamma ** 2 - 2 * x1) % p
    y3 = (gamma * (x1 - x3) - y1) % p
    return x3, y3

def scalarMultiplay(k, gx, gy, a, p):
    """Скалярное умножение точки на число"""
    r = (0, 0)
    b = (gx, gy)
    for bit in bin(k)[2:]:
        r = dotDoubler(r[0], r[1], p, a)
        if bit == '1':
            r = dotAdding(r[0], r[1], b[0], b[1], p, a)
    return r

def encodeNumber(m, gx, gy, k, p, a, c):
    """Шифрование одного символа"""
    R = scalarMultiplay(k, gx, gy, a, p)
    D = scalarMultiplay(c, gx, gy, a, p)
    P = scalarMultiplay(k, D[0], D[1], a, p)
    if P == (0, 0):
        return (0, 0), 0
    e = (m * P[0]) % p
    return R, e

def decodeNumber(e, Rx, Ry, p, a, c):
    """Расшифровка одного символа"""
    Q = scalarMultiplay(c, Rx, Ry, a, p)
    if Q == (0, 0):
        return 0
    inv = fracDivided(1, Q[0], p)
    m = (e * inv) % p
    return m

def validate_curve_point(gx, gy, a, b, p):
    """Проверяет, лежит ли точка на эллиптической кривой"""
    left = (gy ** 2) % p
    right = (gx ** 3 + a * gx + b) % p
    return left == right

def estimate_subgroup_order(gx, gy, a, p, max_iter=1000):
    """Оценивает порядок подгруппы точки G методом последовательного сложения"""
    if gx == 0 and gy == 0:
        return 0
        
    current = (gx, gy)
    order = 1
    
    # Пытаемся найти порядок точки
    for i in range(2, max_iter + 1):
        current = dotAdding(current[0], current[1], gx, gy, p, a)
        order += 1
        
        # Проверяем, достигли ли бесконечности
        if current == (0, 0):
            return order
    
    # Если не нашли за max_iter итераций, возвращаем оценку
    return order

def safe_random_k(subgroup_order):
    """Генерирует k в диапазоне [1, subgroup_order-1]"""
    if subgroup_order < 2:
        raise ValueError("Порядок подгруппы должен быть не менее 2")
    return random.randint(1, subgroup_order - 1)

def clean_message(message):
    """Очищает сообщение: приводит к нижнему регистру и заменяет недопустимые символы"""
    cleaned = []
    for char in message:
        # Приводим к нижнему регистру
        char_lower = char.lower()
        # Заменяем недопустимые символы на пробел
        if char_lower not in RUSSIAN_ALPHABET:
            cleaned.append(' ')
        else:
            cleaned.append(char_lower)
    return ''.join(cleaned)

# Основной цикл
while True:
    print("\n" + "="*50)
    print("СИСТЕМА ШИФРОВАНИЯ НА ЭЛЛИПТИЧЕСКИХ КРИВЫХ")
    print("="*50)
    choice = input("1 - Шифрование | 2 - Расшифрование | 3 - Выход: ")
    
    if choice == "1":
        print("\n[ ШИФРОВАНИЕ СООБЩЕНИЯ ]")
        message = input("Введите сообщение: ")
        p = int(input("Введите p (простое число): "))
        a = int(input("Введите a (коэффициент кривой): "))
        b = int(input("Введите b (коэффициент кривой): "))
        c = int(input("Введите c (открытый ключ получателя): "))
        gx = int(input("Введите координату x для G: "))
        gy = int(input("Введите координату y для G: "))
        
        # Проверка точки на кривой
        if not validate_curve_point(gx, gy, a, b, p):
            print(f"ОШИБКА: Точка G({gx}, {gy}) не принадлежит кривой y² = x³ + {a}x + {b} mod {p}")
            continue
        
        # Оценка порядка подгруппы
        subgroup_order = estimate_subgroup_order(gx, gy, a, p)
        if subgroup_order < 2:
            print("ОШИБКА: Не удалось определить порядок подгруппы для точки G")
            continue
            
        print(f"Порядок подгруппы точки G: ~{subgroup_order}")
        max_k = subgroup_order - 1
        
        # Очистка сообщения
        cleaned_message = clean_message(message)
        if cleaned_message != message:
            print(f"Сообщение очищено: '{message}' -> '{cleaned_message}'")
        
        encrypted_parts = []
        print("\nПроцесс шифрования:")
        for i, char in enumerate(cleaned_message):
            m = char_to_num(char)
            try:
                k = safe_random_k(subgroup_order)
                R, e = encodeNumber(m, gx, gy, k, p, a, c)
                
                print(f"  Символ '{char}': k={k} (1-{max_k}), R=({R[0]}, {R[1]}), e={e}")
                encrypted_parts.append(f"{R[0]},{R[1]},{e}")
            except Exception as ex:
                print(f"  Ошибка шифрования символа '{char}': {ex}")
                encrypted_parts.append("0,0,0")
        
        encrypted_message = ";".join(encrypted_parts)
        print("\nРЕЗУЛЬТАТ ШИФРОВАНИЯ:")
        print(encrypted_message)
    
    elif choice == "2":
        print("\n[ РАСШИФРОВАНИЕ СООБЩЕНИЯ ]")
        encrypted_message = input("Введите зашифрованные данные: ")
        p = int(input("Введите p: "))
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        c = int(input("Введите c (секретный ключ получателя): "))
        
        parts = encrypted_message.split(';')
        decrypted_chars = []
        print("\nПроцесс расшифровки:")
        for i, part in enumerate(parts):
            if not part:
                continue
            try:
                Rx_str, Ry_str, e_str = part.split(',')
                Rx = int(Rx_str)
                Ry = int(Ry_str)
                e = int(e_str)
                
                # Пропускаем невалидные блоки
                if Rx == 0 and Ry == 0 and e == 0:
                    decrypted_chars.append(' ')
                    continue
                
                # Проверка точки на кривой
                if not validate_curve_point(Rx, Ry, a, b, p):
                    print(f"  ОШИБКА: Точка R({Rx}, {Ry}) в блоке {i+1} не принадлежит кривой")
                    decrypted_chars.append('�')
                    continue
                
                m = decodeNumber(e, Rx, Ry, p, a, c)
                char = num_to_char(m)
                
                print(f"  Блок {i+1}: R=({Rx}, {Ry}), e={e} -> m={m} -> '{char}'")
                decrypted_chars.append(char)
            except Exception as ex:
                print(f"  ОШИБКА обработки блока {i+1}: {ex}")
                decrypted_chars.append('�')
        
        decrypted_message = "".join(decrypted_chars)
        print("\nРЕЗУЛЬТАТ РАСШИФРОВКИ:")
        print(decrypted_message)
    
    elif choice == "3":
        print("Выход из программы.")
        sys.exit(0)
    
    else:
        print("Неверный выбор. Попробуйте снова.")