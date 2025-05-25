def get_registers():
    while True:
        rstr = input("Введите ключ 64 символа 0 и 1: ")
        
        if len(rstr) != 64:
            print("Ключ должен быть 64 символов")
            continue

        if not all(char in '01' for char in rstr):
            print("Ключ должен состоять только из 1 и 0")
            continue
        
        r1 = [0]*19
        r2 = [0]*22
        r3 = [0]*23
        r4 = [0]*17
        
        for i in range(64):
            r1t = r1[18]^r1[17]^r1[16]^r1[13]^int(rstr[i])
            r1.insert(0, r1t)
            r1.pop()

            r2t = r2[21]^r2[20]^int(rstr[i])
            r2.insert(0, r2t)
            r2.pop()

            r3t = r3[22]^r3[21]^r3[20]^r3[7]^int(rstr[i])
            r3.insert(0, r3t)
            r3.pop()

            r4t = r4[16]^r4[11]^int(rstr[i])
            r4.insert(0, r4t)
            r4.pop()
        
        print("R1:", r1)
        print("R2:", r2)
        print("R3:", r3)
        print("R4:", r4)
        break
    
    return r1, r2, r3, r4

def gamma(r1, r2, r3, r4):
    for _ in range(99):
        F = (r4[3] & r4[7]) | (r4[3] & r4[10]) | (r4[7] & r4[10])
        
        if r4[10] == F:
            r1t = r1[18]^r1[17]^r1[16]^r1[13]
            r1.insert(0, r1t)
            r1.pop()

        if r4[3] == F:
            r2t = r2[21]^r2[20]
            r2.insert(0, r2t)
            r2.pop()

        if r4[7] == F:
            r3t = r3[22]^r3[21]^r3[20]^r3[7]
            r3.insert(0, r3t)
            r3.pop()

        r4t = r4[16]^r4[11]
        r4.insert(0, r4t)
        r4.pop()

    gam = []
    for _ in range(114):
        F = (r4[3] & r4[7]) | (r4[3] & r4[10]) | (r4[7] & r4[10])
        
        f1 = (r1[12] & r1[14]) | (r1[12] & r1[15]) | (r1[14] & r1[15])

        f2 = (r2[9] & r2[13]) | (r2[9] & r2[16]) | (r2[13] & r2[16])

        f3 = (r3[13] & r4[16]) | (r3[13] & r3[18]) | (r3[16] & r3[18])

        if r4[10] == F:
            r1t = r1[18]^r1[17]^r1[16]^r1[13]
            r1.insert(0, r1t)
            r1.pop()

        if r4[3] == F:
            r2t = r2[21]^r2[20]
            r2.insert(0, r2t)
            r2.pop()

        if r4[7] == F:
            r3t = r3[22]^r3[21]^r3[20]^r3[7]
            r3.insert(0, r3t)
            r3.pop()

        r4t = r4[16]^r4[11]
        r4.insert(0, r4t)
        r4.pop()

        

        gam.append(r1[18]^r2[21]^r3[22]^r4[16]^f1^f2^f3)

    return gam


def encrypt_message(message, binary_array):
    encrypted_array = []
    
    for i, char in enumerate(message):
        ascii_value = ord(char)
        xor_result = ascii_value ^ binary_array[i]
        encrypted_array.append(format(xor_result, '08b'))
        
    return encrypted_array

def decrypt_message(encrypted_array, binary_array):
    decrypted_message = ""
    
    for i, binary_str in enumerate(encrypted_array):
        xor_result = int(binary_str, 2)
        ascii_value = xor_result ^ binary_array[i]
        decrypted_message += chr(ascii_value)
        
    return decrypted_message

while True:
    # Выводим меню с вариантами действий
    print("\nМеню:")
    print("1. Зашифровать сообщение")
    print("2. Расшифровать сообщение")
    print("3. Выход")
    choice = input("Выберите действие: ")  # Запрашиваем выбор пользователя

    if choice == '1':
        # Шифрование сообщения
        r1, r2, r3, r4 = get_registers()  # Получаем регистры
        binary_array = gamma(r1, r2, r3, r4)  # Генерируем гамму
        message = input("Введите сообщение для шифрования: ")  # Запрашиваем сообщение
        encrypted = encrypt_message(message, binary_array)  # Шифруем сообщение
        print("Зашифрованное сообщение:", " ".join(encrypted))  # Выводим результат
    elif choice == '2':
        # Расшифрование сообщения
        r1, r2, r3, r4 = get_registers()  # Получаем регистры
        binary_array = gamma(r1, r2, r3, r4)  # Генерируем гамму
        encrypted_message = input("Введите зашифрованное сообщение (в двоичном формате, разделенное пробелами): ").split()  # Запрашиваем зашифрованное сообщение
        decrypted = decrypt_message(encrypted_message, binary_array)  # Расшифровываем сообщение
        print("Расшифрованное сообщение:", decrypted)  # Выводим результат
    elif choice == '3':
        # Выход из программы
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
