import random  
import binascii  
  
# Определяем алфавит  
alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  
  
def clearCrypte(text):  
    """  
    Предобработка текста для шифрования:  
    - Приводит текст к нижнему регистру.  
    - Заменяет точки и запятые на 'тчк' и 'зпт'.  
    - Заменяет 'ё' на 'е'.  
    - Заменяет пробелы на 'прб' если длина текста больше 500 символов, иначе удаляет пробелы.  
    """  
    text = text.lower()  
    text = text.replace('.', 'тчк')  
    text = text.replace(',', 'зпт')  
    text = text.replace('ё', 'е')  
    if len(text) > 500:  
        text = text.replace(' ', 'прб')  
    else:  
        text = text.replace(' ', '')  
    return text  
  
def hex_to_str(hex_string):  
    """  
    Преобразует шестнадцатеричное представление строки в обычную строку.  
    """  
    byte_array = bytes.fromhex(hex_string)  
    return byte_array.decode('utf-8')  
  
def clearEncypte(text):  
    """  
    Обратная предобработка текста после расшифрования:  
    - Восстанавливает пробелы, точки и запятые.  
    """  
    if len(text) > 500:  
        text = text.replace('прб', ' ')  
    text = text.replace('тчк', '.')  
    text = text.replace('зпт', ',')  
    return text  
  
def decryption_format(text):  
    """  
    Форматирование текста после расшифрования.  
    """  
    # Пример: удаление лишних символов или форматирование текста  
    return text.strip()  
  
def listalf():  
    """  
    Возвращает список символов алфавита.  
    """  
    return list(alph)  
  
  
# Константы и вспомогательные функции для Магмы  
pi = [[12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1], [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15], [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0], [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11], [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12], [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0], [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7], [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]]  
MASK32 = 2 ** 32 - 1  
  
def t(x):  
    y = 0  
    for i in reversed(range(8)):  
        j = (x >> 4 * i) & 0xf  
        y <<= 4  
        y ^= pi[i][j]  
    return y  
  
def rot11(x):  
    return ((x << 11) ^ (x >> (32 - 11))) & MASK32  
  
def g(x, k):  
    return rot11(t((x + k) % 2 ** 32))  
  
def split(x):  
    L = x >> 32  
    R = x & MASK32  
    return (L, R)  
  
def join_parts(left_part, right_part):  
    return (left_part << 32) ^ right_part  
  
def magma_key_schedule(k):  
    keys = []  
    for i in reversed(range(8)):  
        keys.append((k >> (32 * i)) & MASK32)  
    for i in range(8):  
        keys.append(keys[i])  
    for i in range(8):  
        keys.append(keys[i])  
    for i in reversed(range(8)):  
        keys.append(keys[i])  
    return keys  
  
def magma_encrypt(x, k):  
    keys = magma_key_schedule(k)  
    (L, R) = split(x)  
    for i in range(31):  
        (L, R) = (R, L ^ g(R, keys[i]))  
    return format(join_parts(L ^ g(R, keys[-1]), R), '08X')  
  
def magma_decrypt(x, k, mode):  
    res = ''  
    L, R = int(x[0]) >> 32, int(x[0]) & MASK32  
    for j in range(31):  
        (L, R) = (R, L ^ g(R, k[j]))  
    if mode == 1:  
        result = format(join_parts(L ^ g(R, k[-1]), R), 'x')  
        res += hex_to_str(result)  
    elif mode == 2:  
        return format(join_parts(L ^ g(R, k[-1]), R), "0x")  
    return res  
  
while True:
    secet = int(input("Введите режим работы(1 - Шифрование, 2 - Расшифровка, 3 - выход из программы): "))  
    if secet == 1:  
        shifr = ""  
        text = str(input("Введите текст: "))  
        text = clearCrypte(text)  
        key = int('ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff', 16)  
        mode = int(input("Введите режим работы(1 - текст, 2 - ГОСТ): "))  
        if len(text) % 4 != 0:  
            for i in range(4 - len(text) % 4):  
                text += str(alph[random.randint(0, 31)])  
        if mode == 1:  
            while len(text) > 0:
                text_16 = int(text[:4].encode('utf-8').hex(), 16)  
                text = text[4:]  
                shifr += magma_encrypt(text_16, key) + " "  
            print(shifr) 
        elif mode == 2:  
            text = int(text, 16)  
            print(magma_encrypt(text, key))  
    elif secet == 2:  
        res = ""  
        text = str(input("Введите текст: "))  
       
        mode = int(input("Введите режим работы(1 - текст , 2 - ГОСТ): "))  
        key = magma_key_schedule(int('ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff', 16))  
        key.reverse()  
        text = text.split()  
        text = [int(h, 16) for h in text]  
        for i in range(len(text)):  
            dec_text = [text[i]]  
            res += magma_decrypt(dec_text, key, mode)  
        print(clearEncypte(res))  
    if secet == 3:
        break
  


# text - fedcba9876543210
# key - ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff
# untext - 4ee901e5c2d8ca3d