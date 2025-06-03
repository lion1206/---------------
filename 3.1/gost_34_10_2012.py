import random
import sys

# --- Арифметика точек на эллиптической кривой ---

def mod_inverse(a, p):
    """Обратный элемент к a по модулю p."""
    if a == 0:
        raise ValueError("Деление на ноль")
    return pow(a, -1, p)

def is_on_curve(P, a, b, p):
    """Проверяет, лежит ли точка P на кривой y^2 = x^3 + a*x + b mod p"""
    if P == (0, 0):  # Точка в бесконечности
        return True
    x, y = P
    left = pow(y, 2, p)
    right = (pow(x, 3, p) + a * x + b) % p
    return left == right

def double_point(P, p, a):
    """Удвоение точки P = (x, y) на кривой y^2 = x^3 + a x + b mod p."""
    if P == (0, 0):
        return (0, 0)
    x, y = P
    if y == 0:
        return (0, 0)
    try:
        num = (3 * pow(x, 2, p) + a) % p
        den = (2 * y) % p
        L = (num * mod_inverse(den, p)) % p
        x_res = (pow(L, 2, p) - 2 * x) % p
        y_res = (L * (x - x_res) - y) % p
        return (x_res, y_res)
    except ValueError:
        return (0, 0)

def sum_point(P, Q, p, a):
    """Сумма двух точек P и Q на той же кривой."""
    if P == (0, 0): 
        return Q
    if Q == (0, 0): 
        return P
    if P == Q:
        return double_point(P, p, a)
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return (0, 0)
    try:
        num = (y2 - y1) % p
        den = (x2 - x1) % p
        L = (num * mod_inverse(den, p)) % p
        x_res = (pow(L, 2, p) - x1 - x2) % p
        y_res = (L * (x1 - x_res) - y1) % p
        return (x_res, y_res)
    except ValueError:
        return (0, 0)

def mul_point(k, P, a, p):
    """Умножение точки P на скаляр k методом double-and-add."""
    if not is_on_curve(P, a, b, p):
        raise ValueError("Точка не лежит на кривой")
    
    R = (0, 0)
    Q = P
    while k > 0:
        if k & 1:
            R = sum_point(R, Q, p, a)
        Q = double_point(Q, p, a)
        k >>= 1
    return R

# --- Проверка простоты числа ---
def is_prime(n, k=5):
    """Тест Миллера-Рабина на простоту"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False
    
    # Записываем n-1 как d*2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for __ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

# --- ГОСТ Р 34.10-94: подпись и проверка ---

def gost_sign(e, x, G, q, p, a):
    """
    Формирование подписи (r, s):
      r = (a^k mod p) mod q
      s = (x·r + k·e) mod q
    """
    if not (1 < x < q):
        raise ValueError("Неверный секретный ключ x")
    
    for _ in range(100):  # Ограничим количество попыток
        k = random.SystemRandom().randint(2, q-1)
        print("k = ", k)
        C = mul_point(k, G, a, p)
        r = C[0] % q
        if r == 0:
            continue
        try:
            s = (x * r + k * e) % q
        except:
            continue
        if s == 0:
            continue
        return r, s
    raise RuntimeError("Не удалось создать подпись")

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
    try:
        e_inv = pow(e, q-2, q)  # e^{-1} mod q
    except ValueError:
        return False

    # 3) вычисляем u1 и u2
    u1 = (s * e_inv) % q
    print("u1 = ", u1)
    u2 = (-r * e_inv) % q
    print("u2 = ", u2)

    # 4) домножаем точки
    try:
        P1 = mul_point(u1, G, a, p)  # [u1]·G
        print("P1 = ", P1)
        P2 = mul_point(u2, Y, a, p)  # [u2]·Y
        print("P2 = ", P2)
    except ValueError:
        return False

    # 5) складываем их
    P = sum_point(P1, P2, p, a)
    print("P =", P)

    # 6) сравниваем
    print(P[0], "mod", q, "==", r)
    return (P[0] % q) == r

# --- Хеш-функция ---
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ., "

def hash(mes, N):
    """Упрощенная хеш-функция для демонстрации"""
    mes_upper = mes.upper()
    h = 0
    for i in range(len(mes_upper)):
        try:
            char_index = alphabet.index(mes_upper[i]) + 1
            h = (h + char_index)**2 % N
        except ValueError:
            print(f"Внимание: символ '{mes_upper[i]}' не найден в алфавите и будет пропущен")
            continue
    return h

def estimate_subgroup_order(gx, gy, a, p, max_iter=1000):
    """Оценивает порядок подгруппы точки G методом последовательного сложения"""
    if gx == 0 and gy == 0:
        return 0
        
    current = (gx, gy)
    order = 1
    
    # Пытаемся найти порядок точки
    for i in range(2, max_iter + 1):
        current = sum_point(current, (gx, gy), p, a)
        order += 1
        
        # Проверяем, достигли ли бесконечности
        if current == (0, 0):
            return order
    
    # Если не нашли за max_iter итераций, возвращаем оценку
    return order

# --- Основная программа ---
if __name__ == "__main__":
    try:
        # Ввод параметров кривой
        print("Введите параметры эллиптической кривой:")
        p = int(input("Модуль p (простое число): "))
        if not is_prime(p):
            raise ValueError("p должно быть простым числом")
        
        a = int(input("Коэффициент a: "))
        b = int(input("Коэффициент b: "))
        
        print("\nВведите параметры базовой точки G:")
        Gx = int(input("x-координата: "))
        Gy = int(input("y-координата: "))
        G = (Gx, Gy)
        
        if not is_on_curve(G, a, b, p):
            raise ValueError("Точка G не лежит на кривой")
        
        q = estimate_subgroup_order(Gx, Gy, a, p)
        
        
        # Ввод секретного ключа
        x = int(input("\nВведите секретный ключ x (1 < x < q): "))
        if not (1 < x < q):
            raise ValueError("x должно быть в диапазоне (1, q)")
        
        # Вычисление публичного ключа
        Y = mul_point(x, G, a, p)
        print(f"\nПубличный ключ Y = {Y}")
        
        # Ввод сообщения
        msg = input("\nВведите сообщение для подписи: ")
        e = hash(msg, p)
        print(f"Хеш сообщения e = {e}")
        
        # Формирование подписи
        r, s = gost_sign(e, x, G, q, p, a)
        print(f"\nПодпись:\nr = {r}\ns = {s}")
        
        # Проверка подписи
        valid = gost_verify(e, r, s, Y, G, q, p, a)
        print(f"\nРезультат проверки: {'ПОДПИСЬ ВЕРНА' if valid else 'ПОДПИСЬ НЕВЕРНА'}")
    
    except ValueError as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")
        sys.exit(1)