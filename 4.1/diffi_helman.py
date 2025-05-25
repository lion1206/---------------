def mod_exp(base, exp, mod):  # Функция для быстрого возведения в степень по модулю 
    result = 1 
    while exp > 0: 
        if exp % 2 == 1:  # если exp нечетное 
            result = (result * base) % mod 
        base = (base * base) % mod 
        exp //= 2 
    return result 
 
def dif_man(): 
    n = int(input("Введите общее число n (простое число): "))  
 
    while True: 
        a = int(input(f"Введите общее число a (1 < a < {n}): ")) 
        if 1 < a < n: 
            break 
        else: 
            print(f"a должно быть в диапазоне (2, {n})") 
            continue 
 
    while True: 
        ka = int(input(f"Введите число Ka для первого пользователя (2, {n-1}): ")) 
        if 2 <= ka < n: 
            break 
        else: 
            print(f"Ka должно быть в диапазоне (2, {n-1})") 
            continue 
 
    while True: 
        kb = int(input(f"Введите число Kb для второго пользователя (2, {n-1}): ")) 
        if 2 <= kb < n: 
            break 
        else: 
            print(f"Kb должно быть в диапазоне (2, {n-1})") 
            continue 
     
    # Вычисляем открытые ключи 
    Ya = mod_exp(a, ka, n)  # a^ka mod n 
    Yb = mod_exp(a, kb, n)  # a^kb mod n 
 
    print(f"\nОткрытый ключ первого пользователя (Ya): {Ya}") 
    print(f"Открытый ключ второго пользователя (Yb): {Yb}") 
 
    # Вычисляем общий секретный ключ 
    secret_A = mod_exp(Yb, ka, n)  # Yb^ka mod n 
    secret_B = mod_exp(Ya, kb, n)  # Ya^kb mod n 
 
    if secret_A != secret_B: 
        print("\nОшибка: ключи не совпали! Проверьте входные данные.") 
    elif secret_A == 1 or secret_B == 1: 
        print("\nобщий ключ равен 1. Это недопустимо!") 
    if Ya == secret_A or Yb == secret_B or Yb == secret_A or Ya == secret_B:
        print("Секретные и открытые ключи не должны быть равны")
    else: 
        print(f"\nОбщий секретный ключ: {secret_A}") 
 
    
while True:
    repeat = int(input("1 - запуск | 2 - выход: "))
    if repeat == 1:
        dif_man()
    elif repeat == 2:
        break
    if repeat != 1 or repeat != 2:
        print("Введите 1 или 2")