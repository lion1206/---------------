import binascii
from copy import copy
from memory_profiler import memory_usage

from tables import Tables  

class GOST3412_2015:
    tables = None  

    def __init__(self):
        self.tables = Tables()  

    def start_encrypt(self, message, start_key):
        # Разделение  по 16 бит
        round_key = [start_key[:16], start_key[16:]]
        # Генерация раундовых ключей
        round_keys = round_key + self.generate_key(round_key)
        # Шифрование сообщения с использованием раундовых ключей
        return self.encrypt(message, round_keys)

    def start_decrypt(self, cipher, start_key):
       
        round_key = [start_key[:16], start_key[16:]]
        # Генерация раундовых ключей
        round_keys = round_key + self.generate_key(round_key)
        # Расшифрование сообщения с использованием раундовых ключей
        return self.decrypt(cipher, round_keys)

    def generate_key(self, round_key):
        round_keys = []
        for i in range(4):
            for k in range(8):
                # Применение функции Фейстеля для генерации ключей
                round_key = self.feistel(self.tables.c[8 * i + k], round_key)
            # Добавление сгенерированных ключей в список
            round_keys.append(round_key[0])
            round_keys.append(round_key[1])
        return round_keys

    def feistel(self, c, k):
        # Применение операции XOR (x_box) к константе и ключу
        tmp = self.x_box(c, k[0])
        # Применение S-блока (
        tmp = self.s_box(tmp)
        # Применение L-блока (линейное преобразование)
        tmp = self.L_box(tmp)
        # Применение операции XOR (x_box) к результату и второму ключу
        tmp = self.x_box(tmp, k[1])
        return [tmp, k[0]]

    # x_box: k = k xor a (операция XOR между двумя массивами байт)
    def x_box(self, k, a):
        tmp = copy(k)  # Создание копии массива k
        for i in range(0, len(k)):
            tmp[i] ^= a[i]  # Применение XOR к каждому байту
        return tmp

    # S-блок: замена каждого байта по таблице pi
    def s_box(self, a):
        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(a)):
            res[i] = self.tables.pi[a[i]]  # Замена байта по таблице pi
        return res

    # Обратный S-блок: замена каждого байта по таблице pi_inv
    def s_box_inv(self, a):
        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(a)):
            res[i] = self.tables.pi_inv[a[i]]  # Замена байта по таблице pi_inv
        return res

    # L-блок: линейное преобразование
    def L_box(self, a):
        for i in range(len(a)):
            a = self.R_box(a)  # Применение R-блока 16 раз
        return a

    # Обратный L-блок: обратное линейное преобразование
    def L_box_inv(self, a):
        for i in range(len(a)):
            a = self.R_box_inv(a)  # Применение обратного R-блока 16 раз
        return a

    # R-блок: сдвиг и применение l_box
    def R_box(self, a):
        return [self.l_box(a)] + a[:-1]  # Сдвиг массива и добавление результата l_box

    # Обратный R-блок: обратный сдвиг и применение l_box
    def R_box_inv(self, a):
        return a[1:] + [self.l_box(a[1:] + [a[0]])]  # Обратный сдвиг и добавление результата l_box

    # l_box: линейное преобразование, используемое в R-блоке
    def l_box(self, a):
        coef = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
        mul_coef = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, len(coef)):
            mul_coef[i] = self.tables.mul_table[a[i]][coef[i]]  # Умножение байт по таблице
        res = 0
        for i in mul_coef:
            res ^= i  # Применение XOR ко всем результатам умножения
        return res

    # Шифрование сообщения
    def encrypt(self, message, round_keys):
        tmp = message
        for i in range(9):
            tmp = self.x_box(tmp, round_keys[i])  # Применение XOR с раундовым ключом
            tmp = self.s_box(tmp)  # Применение S-блока
            tmp = self.L_box(tmp)  # Применение L-блока
        tmp = self.x_box(tmp, round_keys[9])  # Финальное применение XOR с последним ключом
        return tmp

    # Расшифрование сообщения
    def decrypt(self, cipher, round_keys):
        tmp = cipher
        for i in range(9, 0, -1):
            tmp = self.x_box(tmp, round_keys[i])  # Применение XOR с раундовым ключом
            tmp = self.L_box_inv(tmp)  # Применение обратного L-блока
            tmp = self.s_box_inv(tmp)  # Применение обратного S-блока
        tmp = self.x_box(tmp, round_keys[0])  # Финальное применение XOR с первым ключом
        return tmp


while True:
    algo = GOST3412_2015()  # Создание экземпляра класса GOST3412_2015
    
    choice = input('Выберите действие (1-зашифровать, 2-расшифровать):')  # Получение выбора пользователя
    
    if choice == '1':
        mtest = list(binascii.unhexlify(input("Введите текст для шифрования: ")))  # Преобразование hex-строки в байты
        
        ktest = list(binascii.unhexlify(input('Введите ключ (в hex): ')))  # Преобразование hex-строки в байты
        
        print('Зашифрованный текст:')
        ctest = algo.start_encrypt(mtest, ktest)  # Шифрование сообщения
        print(binascii.hexlify(bytearray(ctest)).decode())  # Вывод зашифрованного текста в hex
        
    elif choice == '2':
        ctest = list(binascii.unhexlify(input('Введите зашифрованный текст: ')))  # Преобразование hex-строки в байты
        ktest = list(binascii.unhexlify(input('Введите ключ (в hex): ')))  # Преобразование hex-строки в байты
        
        print('Расшифрованный текст:')
        mtest = algo.start_decrypt(ctest, ktest)  # Расшифрование сообщения
        print(binascii.hexlify(bytearray(mtest)).decode())  # Вывод расшифрованного текста в hex
        
    else:
        print('Неверный выбор')
        break
    
    



# Примеры использования:
# text - 1122334455667700ffeeddccbbaa9988
# key - 8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef
# untext - 7f679d90bebc24305a468d42b9d4edcd
