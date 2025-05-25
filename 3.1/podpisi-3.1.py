import math
import random

# Алфавит для хеширования сообщения
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"

# Функция для вычисления хеша сообщения
def hash(mes, N):
    h = 0
    for i in range(len(mes)):
        h = (h + (alphabet.index(mes[i])+1))**2 % N  # Хеширование символа и обновление значения хеша
    return h

# Функция для проверки, является ли число простым
def is_prime(n):  
    if n <= 1:  
        return False  
    for i in range(2, int(n**0.5) + 1):  
        if n % i == 0:  
            return False  
    return True  

# Функция для проверки, являются ли два числа взаимно простыми
def is_coprime(x, y):
    return math.gcd(x, y) == 1

# Функция для нахождения обратного элемента по модулю (для RSA)
def f_d(e, N):
    for i in range(N):
        if e*i % N == 1:
            return i

# Расширенный алгоритм Евклида для нахождения НОД и коэффициентов
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функция для нахождения модульного обратного элемента
def modular_inverse(a, p):
    gcd, x, _ = extended_gcd(a, p)
    if gcd != 1:
        raise ValueError(f"Обратного значения для {a} не существует по модулю {p}")
    else:
        return x % p

# Функция для решения линейного сравнения ax ≡ b mod p
def solve_congruence(a, b, p):
    a_inv = modular_inverse(a, p)  # Находим обратное значение a по модулю p
    x = (a_inv * b) % p  # Находим x
    return x

# Функция для вычисления функции Эйлера (fi)
def fi(n):
    f = n
    if n%2 == 0:
        while n%2 == 0:
            n = n // 2
        f = f // 2
    i = 3
    while i*i <= n:
        if n%i == 0:
            while n%i == 0:
                n = n // i
            f = f // i
            f = f * (i-1)
        i = i + 2
    if n > 1:
        f = f // n
        f = f * (n-1)
    return f

# Функция для реализации алгоритма RSA
def rsa():
    string = input("Введите сообщение: ")
    while True:
        while True:
            P = int(input("Введите число P (простое): "))
            if is_prime(P) == False:
                print("Число должно быть простым")
                continue
            else:
                break

        while True:
            Q = int(input("Введите число Q (простое): "))
            if is_prime(Q) == False:
                print("Число должно быть простым")
                continue
            else:
                break
        N = P*Q
        if N < 32:
            print("P*Q < 32")
            continue
        else:
            break
    f = fi((P)*(Q))
    
    while True:
        e = int(input(f"Введите е, 1 < e < {f} взаимное простое с {f}: "))
        if f_d(e, f) == e:
            print("e не должно быть равно закрытому ключу, выберите другое значение e: ")
            continue
        if is_coprime(f, e) == True:
            break
    d = f_d(e, f)
    print(f"Число N: {N}")
    print(f"Число е: {e}")
    print(f"Число d: {d}")
    m = hash(string, N)
    print(f"Хеш: {m}")
    sig = m**d % N  # Создание подписи
    un_sig = sig**e % N  # Проверка подписи

    print(f"Подпись: {sig}")
    print(f"Проверка подписи (ЗНАЧЕНИЕ ХЭШ): {un_sig}")

# Функция для получения случайного числа k, взаимно простого с fi(P)
def get_k(P): 
    r = fi(P) 
    while True: 
        t = random.randint(2, r) 
        if is_coprime(r, t) == True: 
           return t 
 
 
def is_prime(n): 
    """Проверка, является ли число простым.""" 
    if n < 2: 
        return False 
    for i in range(2, int(math.sqrt(n)) + 1): 
        if n % i == 0: 
            return False 
    return True 
 
def hash(string, P): 
    """Простая хэш-функция для примера.""" 
    return sum(ord(char) for char in string) % P 
 
def get_k(phi): 
    """Генерация случайного числа k, взаимно простого с phi.""" 
    while True: 
        k = random.randint(1, phi - 1)  # Генерация случайного числа от 1 до phi-1 
        if math.gcd(k, phi) == 1:  # Проверка, что k и phi взаимно просты 
            return k 
 
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
 
    print(f"Число Y: {y}") 
    print(f"Число k: {k}") 
 
    a = pow(g, k, P)  # a = g^k mod P 
    print(f"Число a: {a}") 
 
    m = hash(string, P)  # Хэш сообщения 
    print(f"Число m: {m}") 
 
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
 
    print(f"Число b: {bi}") 
    print(f"Подпись: ( {bi}, ( {a} )") 
 
    # Проверка подписи 
    a1 = pow(y, a, P) * pow(a, bi, P) % P 
    a2 = pow(g, m, P) 
    print(f"Фрагмент А1: {a1}") 
    print(f"Фрагмент А2: {a2}") 
 
    if a1 == a2: 
        print("Подпись верная") 
    else: 
        print("Подпись неверна!") 
 
 

 
while True:

    print("Выберите подпись (1 - RSA, 2 - ElGamal, 3 - выход из программы): ") 
    ch = int(input()) 
 
    if ch == 1: 
        rsa() 
    elif ch == 2: 
        el_sig()
    elif ch == 3:
        break