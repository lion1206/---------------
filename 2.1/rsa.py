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
        if f_d(e, f) == e:
            print("e не должно быть равно закрытому ключу, выберите другое значение e: ")
            continue
        if is_coprime(f, e):
            break
        
        
    d = f_d(e, f)
    print(f"Открытый ключ (e={e}, N={N}), Закрытый ключ d={d}")
    fin = [(alphabet.index(c) ** e) % N for c in string]
    return fin

def rsaun(string):
    N = int(input("Введите число N: "))
    d = int(input("Введите d: "))
    decoded = [(val ** d) % N for val in string]
    return [alphabet[i] for i in decoded]


while True:
    choice = int(input("Выберите действие (1 - зашифровать, 2 - расшифровать, 3 - выход из программы): "))
    if choice == 1:
        nn = rsa()
        print(f"Зашифрованное сообщение: {nn} ")
    if choice == 2:
        un = rsaun(nn)
        print(f"Зашифрованное сообщение: {un} ")
    elif choice == 3:
        break

