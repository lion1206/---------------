import math
import random

# Функция для проверки, является ли число простым
def is_prime(n): 
    """Проверка, является ли число простым.""" 
    if n < 2: 
        return False 
    for i in range(2, int(math.sqrt(n)) + 1): 
        if n % i == 0: 
            return False 
    return True 

# Алфавит для хеширования сообщения (все символы в верхнем регистре)
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ., "

# Функция для вычисления хеша сообщения
def hash(mes, N):
    # Переводим сообщение в верхний регистр
    mes_upper = mes.upper()
    h = 0
    for i in range(len(mes_upper)):
        try:
            # Ищем символ в алфавите (уже в верхнем регистре)
            char_index = alphabet.index(mes_upper[i]) + 1
            h = (h + char_index)**2 % N
        except ValueError:
            # Если символа нет в алфавите, пропускаем его
            print(f"Внимание: символ '{mes_upper[i]}' не найден в алфавите и будет пропущен")
            continue
    return h

# Функция для генерации случайного числа k, взаимно простого с phi
def get_k(phi): 
    """Генерация случайного числа k, взаимно простого с phi.""" 
    while True: 
        k = random.randint(1, phi - 1)
        if math.gcd(k, phi) == 1:
            return k 

# Функция для реализации алгоритма ElGamal
def el_sig(): 
    string = input("Введите сообщение: ")
    
    while True: 
        P = int(input("Введите число P (простое): ")) 
        if not is_prime(P): 
            print("Число должно быть простым") 
            continue 
        if P < 32: 
            print("Число должно быть больше 32") 
            continue 
        else: 
            break 
 
    while True: 
        g = int(input("Введите число g: ")) 
        if 1 < g < P: 
            break 
        else: 
            print(f"1 < g < {P}") 
 
    while True: 
        x = int(input("Введите число x: ")) 
        if 1 < x < P: 
            break 
        else: 
            print(f"1 < x < {P}") 
 
    y = pow(g, x, P)  # y = g^x mod P
    phi = P - 1  # Функция Эйлера для простого P 
    k = get_k(phi)  # Генерация k, взаимно простого с phi 
 
    print(f"\nПубличный ключ Y: {y}") 
    print(f"Случайное число k: {k}") 
 
    a = pow(g, k, P)  # a = g^k mod P 
    print(f"Первая часть подписи a: {a}") 
 
    m = hash(string, P)  # Хэш сообщения 
    print(f"\nХэш сообщения: {m}") 
 
    # Поиск числа b 
    bi = 0 
    for i in range(P): 
        if P - 1 == m: 
            if (x * a + k * i) % (P - 1) == 0: 
                bi = i 
                break 
        if (x * a + k * i) % (P - 1) == m: 
            bi = i 
            break 
 
    print(f"Вторая часть подписи b: {bi}") 
    print(f"\nИтоговая подпись: ({a}, {bi})") 
 
    # Проверка подписи 
    a1 = (pow(y, a, P) * pow(a, bi, P)) % P 
    a2 = pow(g, m, P) 
    print(f"\nПроверка подписи:")
    print(f"A1 = {a1}")
    print(f"A2 = {a2}") 
 
    if a1 == a2: 
        print("\nРезультат: Подпись верна!") 
    else: 
        print("\nРезультат: Подпись неверна!") 

if __name__ == "__main__":
    print("Электронная подпись ElGamal")
    print("=" * 30)
    el_sig()