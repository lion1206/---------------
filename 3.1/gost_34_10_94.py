import math
import random

# Алфавит для хэширования сообщения
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"

# Простейшая (образовательная) хеш-функция
def hash_message(mes, P):
    h = 0
    for ch in mes:
        idx = alphabet.find(ch)
        if idx < 0:
            raise ValueError(f"Символ '{ch}' не в алфавите")
        # добавляем (позиция в алфавите +1), возводим в квадрат и берём mod P
        h = (h + (idx+1))**2 % P
    return h

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r = int(n**0.5)
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

def get_q(P):
    return [i for i in range(2, P) if (P-1) % i == 0 and is_prime(i)]

def get_a(P, Q):
    return [i for i in range(2, P-1) if pow(i, Q, P) == 1]

def gost():
    # 1. Ввод сообщения
    msg = input("Введите сообщение (только заглавные кириллические буквы): ")

    # 2. Выбор P
    while True:
        P = int(input("Введите P > 32: "))
        if not is_prime(P):
            print("P должно быть простым")
        if P < 32:
            print( "P должно быть больше 32")
        else:
            break

    # 3. Выбор Q
    q_cand = get_q(P)
    print("Возможные Q (делители P-1):", q_cand)
    while True:
        Q = int(input("Выберите Q из списка: "))
        if Q not in q_cand:
            print("Q должно быть простым делителем P-1")
        else:
            break

    # 4. Выбор a
    a_cand = get_a(P, Q)
    print("Возможные a (порядок Q):", a_cand[:10], "…")
    while True:
        a = int(input("Выберите a (1 < a < P-1 и a^Q mod P = 1): "))
        if a <= 1 or a >= P-1 or pow(a, Q, P) != 1:
            print("Неправильное a")
        else:
            break

    # 5. Ввод закрытого ключа x
    while True:
        x = int(input(f"Введите x (1 < x < Q={Q}): "))
        if not (1 < x < Q):
            print("x должно быть в диапазоне 2..Q-1")
        else:
            break

    # 6. Публичный ключ
    y = pow(a, x, P)
    print(f"Публичный ключ y = {y}")

    # 7. Хеширование
    m = hash_message(msg, P)
    if m % Q == 0:
        m = 1
    print(f"H(m) mod Q = {m}")

    # 8. Подпись
    while True:
        k = random.randint(1, Q-1)
        r = pow(a, k, P) % Q
        if r == 0:
            continue
        s = (x * r + k * m) % Q
        if s == 0:
            continue
        break
    print(f"Подпись: r = {r}, s = {s}")

    # 9. Проверка
    v = pow(m, Q-2, Q)
    z1 = (s * v) % Q
    z2 = ((Q - r) * v) % Q
    u = (pow(a, z1, P) * pow(y, z2, P) % P) % Q
    print(f"v = {v}\nz1 = {z1}, z2 = {z2}\nu = {u}")
    print("Проверка:", "ВЕРНО" if u == r else "НЕВЕРНО")

if __name__ == "__main__":
    gost()
