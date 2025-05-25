import random

# --- Арифметика точек на эллиптической кривой ---

def mod_inverse(a, p):
    """Обратный элемент к a по модулю p."""
    return pow(a, -1, p)

def double_point(P, p, a):
    """Удвоение точки P = (x, y) на кривой y^2 = x^3 + a x + b mod p."""
    if P[1] == 0:
        return (0, 0)
    num = (3 * P[0]**2 + a) % p
    den = (2 * P[1]) % p
    L = (num * mod_inverse(den, p)) % p
    x = (L**2 - 2*P[0]) % p
    y = (L*(P[0] - x) - P[1]) % p
    return (x, y)

def sum_point(P, Q, p):
    """Сумма двух точек P и Q на той же кривой."""
    if P == (0, 0): return Q
    if Q == (0, 0): return P
    if P == Q:
        return double_point(P, p, a)
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return (0, 0)
    num = (Q[1] - P[1]) % p
    den = (Q[0] - P[0]) % p
    L = (num * mod_inverse(den, p)) % p
    x = (L**2 - P[0] - Q[0]) % p
    y = (L*(P[0] - x) - P[1]) % p
    return (x, y)

def mul_point(k, P, a, p):
    """Умножение точки P на скаляр k методом double-and-add."""
    R = (0, 0)
    Q = P
    while k > 0:
        if k & 1:
            R = sum_point(R, Q, p)
        Q = double_point(Q, p, a)
        k >>= 1
    return R

# --- ГОСТ Р 34.10-94: подпись и проверка ---

def gost_sign(e, x, G, q, p, a):
    """
    Формирование подписи (r, s):
      r = (a^k mod p) mod q
      s = (x·r + k·e) mod q
    """
    while True:
        k = random.randint(2, q-1)
        print("k = ", k)
        C = mul_point(k, G, a, p)
        r = C[0] % q
        if r == 0:
            continue
        s = (x * r + k * e) % q
        if s == 0:
            continue
        return r, s

def gost_verify(e, r, s, Y, G, q, p, a):
    """
    Проверка подписи по ГОСТ Р 34.10-94 (эллиптический вариант):
      u1 =  s * e^{-1} mod q
      u2 = -r * e^{-1} mod q
      P = [u1]G + [u2]Y
      проверка: r == P.x mod q
    """
    # 1) базовая проверка диапазонов
    if not (0 < r < q and 0 < s < q):
        return False

    # 2) вычисляем обратное к e по модулю q
    e_inv = pow(e, q-2, q)  # e^{-1} mod q

    # 3) вычисляем u1 и u2
    u1 = ( s * e_inv ) % q
    print("u1 = ", u1)
    u2 = (-r * e_inv ) % q
    print("u2 = ", u2)

    # 4) домножаем точки
    P1 = mul_point(u1, G, a, p)  # [u1]·G
    print("P1 = ", P1)
    P2 = mul_point(u2, Y, a, p)  # [u2]·Y
    print("P2 = ", P2)

    # 5) складываем их
    P = sum_point(P1, P2, p)
    print(P)

    # 6) сравниваем
    print(P[0], "mod", q, "==",r)
    return (P[0] % q) == r

# --- Основная программа ---

# Ввод параметров кривой
p  = int(input("Введите модуль p (простое число): "))
a  = int(input("Введите коэффициент a: "))
b  = int(input("Введите коэффициент b: "))
Gx = int(input("Введите x-координату точки G: "))
Gy = int(input("Введите y-координату точки G: "))
G  = (Gx, Gy)
q  = int(input("Введите порядок точки G (q): "))

# Ввод секретного ключа x
x = int(input("Введите секретный ключ x (1 < x < q): "))

# Вычисление публичного ключа Y = a^x mod p
Y = mul_point(x, G, a, p)
print(f"\nПубличный ключ Y = {Y}")

# Ввод сообщения и хеширование (упрощённо)
msg = input("\nВведите сообщение для подписи: ")
e = sum(ord(ch) for ch in msg) % q
print(f"Хеш e = {e}")

# Формирование подписи
r, s = gost_sign(e, x, G, q, p, a)
print(f"\nПодпись:\nr = {r}\ns = {s}")

# Проверка подписи
valid = gost_verify(e, r, s, Y, G, q, p, a)
print(f"\nРезультат проверки: {'ПОДПИСЬ ВЕРНА' if valid else 'ПОДПИСЬ НЕВЕРНА'}")
