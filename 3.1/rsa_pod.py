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

if __name__ == "__main__":
    rsa()