KEY_SIZE = 32  # 32 байта = 256 бит
IV_SIZE = 8    # 8 байт = 64 бит

def bytes_to_hex(data: bytes) -> str:
    return data.hex()


def hex_to_bytes(hex_string: str) -> bytes:
    try:
        return bytes.fromhex(hex_string)
    except ValueError:
        print("Ошибка: Некорректная HEX-строка.")
        return b""


def generate_gamma(length: int, key: bytes, iv: bytes) -> bytes:
    gamma = bytearray()
    counter = bytearray(iv)
    for i in range(length):
        gamma.append(key[i % len(key)] ^ counter[i % len(counter)])
        counter[i % len(counter)] = (counter[i % len(counter)] + 1) % 256
    return bytes(gamma)


def process_data(data: bytes, key: bytes, iv: bytes) -> bytes:
    gamma = generate_gamma(len(data), key, iv)
    return bytes(d ^ g for d, g in zip(data, gamma))


while True:
    print("CTR-Шифрование (XOR)")
    print("1. Зашифровать")
    print("2. Расшифровать")
    print("3. Выход")
    choice = input("Выберите действие (1-3): ")

    if choice not in ['1', '2', '3']:
        print("Неверный выбор.")
        break

    
    key = hex_to_bytes(input("Введите ключ (HEX): ").strip())
    iv = hex_to_bytes(input("Введите IV (HEX): ").strip())


    if choice == '1':
        plaintext = input("Введите текст для шифрования: ").encode("utf-8")
        encrypted = process_data(plaintext, key, iv)
        print("Зашифрованные данные (HEX):", bytes_to_hex(encrypted))
    if choice == '2':
        hex_data = input("Введите HEX-строку для расшифровки: ").strip()
        ciphertext = hex_to_bytes(hex_data)
        if not ciphertext:
            break
        decrypted = process_data(ciphertext, key, iv)
        try:
            print("Расшифрованный текст:", decrypted.decode("utf-8"))
        except UnicodeDecodeError:
            print("Результат (бинарные данные):", decrypted)
    if choice == '3':
        break

