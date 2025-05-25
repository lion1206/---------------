def get_r1():
    while True:
        # Запрашиваем у пользователя ключ длиной 64 символа, состоящий из 0 и 1
        rstr = input("Введите ключ 64 символа 0 и 1: ")
        
        # Проверяем длину ключа
        if len(rstr) != 64:
            print("Ключ должен быть 64 символов")
            continue  # Если длина не 64, запрашиваем ключ снова

        # Проверяем, что ключ состоит только из 0 и 1
        if not all(char in '01' for char in rstr):
            print("Ключ должен состоять только из 1 и 0")
            continue  # Если ключ содержит другие символы, запрашиваем снова

        r1 = [0]*19
        r2 = [0]*22
        r3 = [0]*23
        for i in range(64):
            r1t = r1[18]^r1[17]^r1[16]^r1[13]^int(rstr[i]) 
            r1p = r1[18]
            r1.insert(0,r1t)
            r1.pop(19)

            r2t = r2[21]^r2[20]^int(rstr[i]) 
            r2p = r2[21]
            r2.insert(0,r2t)
            r2.pop(22)
            
            r3t = r3[22]^r3[21]^r3[20]^r3[7]^int(rstr[i])
            r3p = r3[22]
            r3.insert(0,r3t)
            r3.pop(23)
            
        print(r1)
        print(r2)
        print(r3)
        

        break


    return r1, r2, r3  # Возвращаем инициализированные регистры


def gamma(r1, r2, r3):
    gam = []  # Список для хранения гаммы (последовательности битов)
    for _ in range(114):  # Генерация 114 бит гаммы
        # Вычисление бита гаммы: XOR последних битов регистров r1, r2 и r3
        gamma_bit = r1[-1] ^ r2[-1] ^ r3[-1]
        gam.append(gamma_bit)  # Добавляем бит гаммы в список

        # Обновление регистров с использованием обратной связи:
        # Для r1: XOR 18-го, 17-го, 16-го и 13-го битов
        feedback_r1 = r1[18] ^ r1[17] ^ r1[16] ^ r1[13]
        # Для r2: XOR 21-го и 20-го битов
        feedback_r2 = r2[21] ^ r2[20]
        # Для r3: XOR 22-го, 21-го, 20-го и 7-го битов
        feedback_r3 = r3[22] ^ r3[21] ^ r3[20] ^ r3[7]

        # Сдвиг регистров:
        # Новый бит добавляется в начало, а последний бит удаляется
        r1 = [feedback_r1] + r1[:-1]  # Сдвиг r1
        r2 = [feedback_r2] + r2[:-1]  # Сдвиг r2
        r3 = [feedback_r3] + r3[:-1]  # Сдвиг r3

    return gam  # Возвращаем сгенерированную гамму


def encrypt_message(message, binary_array):
    encrypted_array = []  # Список для хранения зашифрованных данных
    for i, char in enumerate(message):
        # Преобразуем символ в его ASCII-код
        ascii_value = ord(char)
        # Выполняем XOR между ASCII-кодом и соответствующим битом гаммы
        xor_result = ascii_value ^ binary_array[i]
        # Преобразуем результат в 8-битное двоичное представление и добавляем в список
        encrypted_array.append(format(xor_result, '08b'))
    return encrypted_array  # Возвращаем зашифрованное сообщение


def decrypt_message(encrypted_array, binary_array):
    decrypted_message = ""  # Строка для хранения расшифрованного сообщения
    for i, binary_str in enumerate(encrypted_array):
        # Преобразуем двоичную строку в число
        xor_result = int(binary_str, 2)
        # Выполняем XOR между числом и соответствующим битом гаммы
        ascii_value = xor_result ^ binary_array[i]
        # Преобразуем ASCII-код обратно в символ и добавляем к результату
        decrypted_message += chr(ascii_value)
    return decrypted_message  # Возвращаем расшифрованное сообщение


while True:
    # Выводим меню с вариантами действий
    print("\nМеню:")
    print("1. Зашифровать сообщение")
    print("2. Расшифровать сообщение")
    print("3. Выход")
    choice = input("Выберите действие: ")  # Запрашиваем выбор пользователя

    if choice == '1':
        # Шифрование сообщения
        r1, r2, r3 = get_r1()  # Получаем регистры
        binary_array = gamma(r1, r2, r3)  # Генерируем гамму
        message = input("Введите сообщение для шифрования: ")  # Запрашиваем сообщение
        encrypted = encrypt_message(message, binary_array)  # Шифруем сообщение
        print("Зашифрованное сообщение:", " ".join(encrypted))  # Выводим результат
    elif choice == '2':
        # Расшифрование сообщения
        r1, r2, r3 = get_r1()  # Получаем регистры
        binary_array = gamma(r1, r2, r3)  # Генерируем гамму
        encrypted_message = input("Введите зашифрованное сообщение (в двоичном формате, разделенное пробелами): ").split()  # Запрашиваем зашифрованное сообщение
        decrypted = decrypt_message(encrypted_message, binary_array)  # Расшифровываем сообщение
        print("Расшифрованное сообщение:", decrypted)  # Выводим результат
    elif choice == '3':
        # Выход из программы
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")


