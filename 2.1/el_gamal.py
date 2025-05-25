import random
import math

alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"

def is_prime(n):  
    if n <= 1:  
        return False  
    for i in range(2, int(n**0.5) + 1):  
        if n % i == 0:  
            return False  
    return True  

def is_coprime(x, y):
    return math.gcd(x, y) == 1

def fi(n):
    f = n
    if n % 2 == 0:
        while n % 2 == 0:
            n //= 2
        f //= 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            f = f // i * (i - 1)
        i += 2
    if n > 1:
        f = f // n * (n - 1)
    return f

def get_k(P, l):
    r = fi(P)
    ks = []
    while len(ks) < l:
        t = random.randint(1, r)
        if is_coprime(r, t):
            ks.append(t)
    return ks

def el_gamal():
    string = input("Введите сообщение: ")
    while True:
        P = int(input("Введите число P (простое): "))
        if is_prime(P) and P > 32:
            break
        print("Число должно быть простым и больше 32")

    x = int(input("Введите число x: "))
    g = int(input("Введите число g: "))
    y = pow(g, x, P)
    print(f"Открытый ключ y: {y}")

    k = get_k(P, len(string))
    print(f"Рандомизаторы: {k}")

    fin = []
    for i, ch in enumerate(string):
        ind = alphabet.index(ch)
        a = pow(g, k[i], P)
        b = pow(y, k[i], P) * ind % P
        fin.append([a, b])
    return fin

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1

def modular_inverse(a, p):
    g, x, _ = extended_gcd(a, p)
    if g != 1:
        raise ValueError("Обратного значения не существует")
    return x % p

def solve_congruence(a, b, p):
    a_inv = modular_inverse(a, p)
    return (a_inv * b) % p

def get_x(y, g, P):
    for i in range(P):
        if pow(g, i, P) == y:
            return i

def el_gamalun(string):
    while True:
        P = int(input("Введите число P (простое): "))
        if is_prime(P) and P > 32:
            break
        print("Число должно быть простым и больше 32")

    y = int(input("Введите число y: "))
    g = int(input("Введите число g: "))
    x = get_x(y, g, P)

    fin = []
    for a, b in string:
        a_x = pow(a, x, P)
        m = solve_congruence(a_x, b, P)
        fin.append(m)
    return [alphabet[i] for i in fin]

while True:
    choice = int(input("Выберите действие (1 - зашифровать, 2 - расшифровать, 3 - выход из программы): "))
    if choice == 1:
        nn = el_gamal()
        print(f"Зашифрованное сообщение: {nn} ")
    if choice == 2:
        un = el_gamalun(nn)
        print(f"Зашифрованное сообщение: {un} ")
    elif choice == 3:
        break

