import sys
import math

# Алфавит без ё (в нижнем регистре)
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
m = len(alphabet)  # 32

# Функция для подготовки текста
def prepare_text(text):
    text = text.replace(" ", "").lower()  # Приводим к нижнему регистру
    text = text.replace(".", "тчк")
    text = text.replace(",", "зпт")
    text = text.replace("ё", "е")
    return text

# Функция для проверки параметров
def validate_parameters(t0, a, c):
    if not (1 <= t0 <= 32):
        raise ValueError("t0 должно быть в диапазоне от 1 до 32.")
    if not (1 < a <= 32):
        raise ValueError("a должно быть в диапазоне от 1 до 32.")
    if a == 1:
        raise ValueError("a не должно быть равно 1.")
    if not (1 <= c <= 32):
        raise ValueError("c должно быть в диапазоне от 1 до 32.")
    if math.gcd(c, m) != 1:
        raise ValueError("c должно быть взаимно просто с модулем 32.")
    if a % 4 != 1:
        raise ValueError("a должно удовлетворять условию a mod 4 = 1.")
    if a % 2 == 0:
        raise ValueError("a должно быть нечетным числом.")
    if c % 2 == 0:
        raise ValueError("c должно быть нечетным числом.")

# Функция для шифрования
def encrypt(text, t0, a, c):
    text = prepare_text(text)  # Подготавливаем текст
    encrypted_numbers = []
    t_current = t0  # Начинаем с t0
    for char in text:
        char_index = alphabet.find(char)  # Индекс символа в алфавите
        if char_index == -1:
            raise ValueError(f"Символ '{char}' не найден в алфавите.")
        t_next = (t_current * a + c) % m  # Вычисляем следующее t
        encrypted_number = (t_next + char_index) % m  # Зашифрованное значение по модулю 32
        encrypted_numbers.append(f"{encrypted_number:02d}")  # Сохраняем как двузначное число
        t_current = t_next  # Обновляем t_current для следующего символа
    return " ".join(encrypted_numbers)  # Возвращаем строку цифр, разделенных пробелами

# Функция для расшифрования
def decrypt(encrypted_numbers, t0, a, c):
    encrypted_numbers = encrypted_numbers.strip().split(" ")  # Разделяем строку на числа
    decrypted_text = ""
    t_current = t0  # Начинаем с t0
    for number in encrypted_numbers:
        encrypted_number = int(number)  # Преобразуем строку в число
        t_next = (t_current * a + c) % m  # Вычисляем следующее t
        char_index = (encrypted_number - t_next) % m  # Восстанавливаем индекс символа
        if char_index < 0 or char_index >= m:
            raise ValueError(f"Некорректное зашифрованное значение: {encrypted_number}.")
        decrypted_text += alphabet[char_index]
        t_current = t_next  # Обновляем t_current для следующего символа
    return decrypted_text

# Функция для ввода параметра с проверкой
def input_parameter(prompt, validation_func):
    while True:
        try:
            value = int(input(prompt))
            validation_func(value)
            return value
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")


while True:
    print("1. Зашифровать")
    print("2. Расшифровать")
    print("3. Выход")
    choice = input("Выберите действие (1-3): ")

    if choice == "1":
        try:
            # Ввод параметров с проверкой
            t0 = input_parameter("Введите параметр t0 (от 1 до 32): ", lambda x: validate_parameters(x, 5, 1))
            a = input_parameter("Введите параметр a (от 1 до 32, нечетное, a mod 4 = 1): ", lambda x: validate_parameters(1, x, 1))
            c = input_parameter("Введите параметр c (от 1 до 32, нечетное, взаимно простое с 32): ", lambda x: validate_parameters(1, 5, x))
            text = input("Введите текст для шифрования: ")
            encrypted_numbers = encrypt(text, t0, a, c)
            print("Зашифрованный текст: ", encrypted_numbers)
        except Exception as e:
            print(f"Ошибка: {e}")

    elif choice == "2":
        try:
            # Ввод параметров с проверкой
            t0 = input_parameter("Введите параметр t0 (от 1 до 32): ", lambda x: validate_parameters(x, 5, 1))
            a = input_parameter("Введите параметр a (от 1 до 32, нечетное, a mod 4 = 1): ", lambda x: validate_parameters(1, x, 1))
            c = input_parameter("Введите параметр c (от 1 до 32, нечетное, взаимно простое с 32): ", lambda x: validate_parameters(1, 5, x))
            encrypted_numbers = input("Введите шифр: ")
            decrypted_text = decrypt(encrypted_numbers, t0, a, c)
            print("Расшифрованный текст:", decrypted_text)
        except Exception as e:
            print(f"Ошибка: {e}")

    elif choice == "3":
        print("Выход из программы.")
        sys.exit()

    else:
        print("Неверный выбор. Попробуйте снова.")
