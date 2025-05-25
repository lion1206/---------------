def phi(n):
    result = n
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
    if n > 1:
        result -= result // n
    return result

def fracDivided(top, bottom, p):
    if bottom == 0:
        print("Деление на ноль в fracDivided")
        return 0
    # Обратный элемент по модулю
    inv = pow(bottom, phi(p) - 1, p)
    return (top * inv) % p

def dotAdding(x1, y1, x2, y2, p):
    if x1 == 0 and y1 == 0:
        return x2, y2
    if x2 == 0 and y2 == 0:
        return x1, y1
    if x1 == x2 and (y1 + y2) % p == 0:
        return 0, 0

    if x1 != x2:
        gamma = fracDivided(y2 - y1, x2 - x1, p)
    else:
        gamma = fracDivided(3 * x1 ** 2 + 1, 2 * y1, p)

    x3 = (gamma ** 2 - x1 - x2) % p
    y3 = (gamma * (x1 - x3) - y1) % p
    return x3, y3

def dotDoubler(x1, y1, p, a=1):
    if y1 == 0:
        return 0, 0
    gamma = fracDivided(3 * x1 ** 2 + a, 2 * y1, p)
    x3 = (gamma ** 2 - 2 * x1) % p
    y3 = (gamma * (x1 - x3) - y1) % p
    return x3, y3

def scalarMultiplay(k, gx, gy, a, p):
    r = (0, 0)
    b = (gx, gy)
    for bit in bin(k)[2:]:
        r = dotDoubler(*r, p, a)
        if bit == '1':
            r = dotAdding(*r, *b, p)
    return r

def encodeNumber(m, gx, gy, k, p, a, c):
    R = scalarMultiplay(k, gx, gy, a, p)
    D = scalarMultiplay(c, gx, gy, a, p)
    P = scalarMultiplay(k, D[0], D[1], a, p)
    if P == (0, 0):
        print("Точка на бесконечности")
        return 0
    e = (m * P[0]) % p

    print("Вычисления:")
    print(f"G = ({gx}, {gy})")
    print(f"k = {k}, c = {c}")
    print(f"R = kG = {R}")
    print(f"D = cG = {D}")
    print(f"P = kD = {P}")
    print(f"m = {m}")
    print(f"Зашифрованное значение e = (m * Px) mod p = {e}")

    return R, e

def decodeNumber(e, Rx, Ry, p, a, c):
    Rx, Ry, p, a, c = map(int, (Rx, Ry, p, a, c))
    Q = scalarMultiplay(c, Rx, Ry, a, p)
    if Q == (0, 0):
        print("Точка на бесконечности")
        return 0
    inv = fracDivided(1, Q[0], p)
    m = (e * inv) % p

    print("Вычисления Расшифровки:")
    print(f"R = ({Rx}, {Ry})")
    print(f"e = {e}, c = {c}")
    print(f"Q = cR = {Q}")
    print(f"m = {m}")

    return m

# Основной цикл
while True:
    choice = input("1 - Шифрование | 2 - Расшифрование | 3 - Выход: ")
    if choice == "1":
        m = int(input("Введите сообщение: "))
        p = int(input("Введите p: "))
        a = int(input("Введите a: "))
        c = int(input("Введите c (открытый ключ получателя): "))
        k = int(input("Введите k (случайное число): "))
        gx = int(input("Введите координату x для G: "))
        gy = int(input("Введите координату y для G: "))
        R, e = encodeNumber(m, gx, gy, k, p, a, c)
        print(f"Зашифрованные данные:\nR: ({R[0]}, {R[1]}), e: {e}")
    elif choice == "2":
        e = int(input("Введите зашифрованное сообщение e: "))
        p = input("Введите p: ")
        a = input("Введите a: ")
        c = input("Введите c (секретный ключ получателя): ")
        Rx = input("Введите координату x точки R: ")
        Ry = input("Введите координату y точки R: ")
        m = decodeNumber(e, Rx, Ry, p, a, c)
        print(f"Расшифрованное сообщение: {m}")
    elif choice == "3":
        break
    else:
        print("Неверный выбор. Попробуйте снова.")
