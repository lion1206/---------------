import os
import binascii

# --- Константы AES ---
sBox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]
invSBox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]
Rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
Nb = 4  # размер блока для слова 
BLOCK_SIZE_BYTES = 16

# --- Вспомогательные функции ---
def hex_to_bytes(hex_string):
    try:
        return binascii.unhexlify(hex_string)
    except binascii.Error as e:
        raise ValueError(f"Invalid HEX string: {e}")

def bytes_to_hex(byte_array):
    return binascii.hexlify(byte_array).decode('ascii')

def gmul(a, b):
    p = 0
    for _ in range(8):
        if (b & 1) != 0:
            p ^= a
        hi_bit_set = (a & 0x80) != 0
        a <<= 1
        if hi_bit_set:
            a ^= 0x11b 
        b >>= 1
    return p & 0xFF

# --- Основные шаги AES ---
def sub_bytes(state):
    for i in range(len(state)):
        state[i] = sBox[state[i]]

def inv_sub_bytes(state):
    for i in range(len(state)):
        state[i] = invSBox[state[i]]

def shift_rows(state):
    state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]

def inv_shift_rows(state):
    state[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3]

def mix_columns(state):
    for c in range(Nb):
        offset = c * 4
        s0, s1, s2, s3 = state[offset:offset+4]
        state[offset + 0] = gmul(0x02, s0) ^ gmul(0x03, s1) ^ s2 ^ s3
        state[offset + 1] = s0 ^ gmul(0x02, s1) ^ gmul(0x03, s2) ^ s3
        state[offset + 2] = s0 ^ s1 ^ gmul(0x02, s2) ^ gmul(0x03, s3)
        state[offset + 3] = gmul(0x03, s0) ^ s1 ^ s2 ^ gmul(0x02, s3)

def inv_mix_columns(state):
     for c in range(Nb):
        offset = c * 4
        s0, s1, s2, s3 = state[offset:offset+4]
        state[offset + 0] = gmul(0x0e, s0) ^ gmul(0x0b, s1) ^ gmul(0x0d, s2) ^ gmul(0x09, s3)
        state[offset + 1] = gmul(0x09, s0) ^ gmul(0x0e, s1) ^ gmul(0x0b, s2) ^ gmul(0x0d, s3)
        state[offset + 2] = gmul(0x0d, s0) ^ gmul(0x09, s1) ^ gmul(0x0e, s2) ^ gmul(0x0b, s3)
        state[offset + 3] = gmul(0x0b, s0) ^ gmul(0x0d, s1) ^ gmul(0x09, s2) ^ gmul(0x0e, s3)

def add_round_key(state, round_key):
    for i in range(16):
        state[i] ^= round_key[i]

# --- Расширение ключа ---
def sub_word(word):
    return [sBox[b] for b in word]

def rot_word(word):
    return word[1:] + word[:1]

def key_expansion(key_bytes):
    key_size = len(key_bytes)
    if key_size not in [16, 24, 32]:
        raise ValueError("Неправильный ключ. Может быть только 16, 24, или 32 бита.")

    Nk = key_size // 4 
    Nr = {16: 10, 24: 12, 32: 14}[key_size] 

    key_words = [list(key_bytes[i*4:(i+1)*4]) for i in range(Nk)]
    w = list(key_words) 

    for i in range(Nk, Nb * (Nr + 1)):
        temp = list(w[i - 1]) 
        if i % Nk == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] ^= Rcon[i // Nk]
        elif Nk > 6 and i % Nk == 4: 
            temp = sub_word(temp)

        prev_key_word = w[i - Nk]
        w.append([prev_key_word[b] ^ temp[b] for b in range(4)])

    
    round_keys = []
    for r in range(Nr + 1):
        round_key = []
        for c in range(Nb):
            round_key.extend(w[r * Nb + c])
        round_keys.append(round_key)

    return round_keys, Nr

# --- Блочное шифрование/расшифрование ---
def cipher(input_bytes, round_keys, Nr):
    """Шифрует один 16-байтный блок."""
    if len(input_bytes) != 16: raise ValueError("Блок может быть только 16 бит.")
    state = list(input_bytes) # Работаем с изменяемым списком
    add_round_key(state, round_keys[0])
    for round_num in range(1, Nr):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[round_num])
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[Nr])
    return bytes(state) # Возвращаем неизменяемые байты

def inv_cipher(input_bytes, round_keys, Nr):
    """Расшифровывает один 16-байтный блок."""
    if len(input_bytes) != 16: raise ValueError("Блок может быть только 16 байт.")
    state = list(input_bytes)
    add_round_key(state, round_keys[Nr])
    for round_num in range(Nr - 1, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[round_num])
        inv_mix_columns(state)
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])
    return bytes(state)

# --- Режим CTR ---
def aes_ctr_process(data_bytes: bytes, key_bytes: bytes, iv_bytes: bytes) -> bytes | None:
    """
    Шифрует/расшифровывает данные в режиме CTR AES.
    Шифрование и расшифрование в CTR идентичны.

    Args:
        data_bytes (bytes): Входные данные.
        key_bytes (bytes): Ключ (16, 24 или 32 байта).
        iv_bytes (bytes): IV/Nonce (16 байт).

    Returns:
        bytes | None: Результат или None при ошибке.
    """
    try:
        if len(iv_bytes) != 16:
            raise ValueError("IV для AES CTR может быть только 16 байт (128 bits).")

        round_keys, Nr = key_expansion(key_bytes)

        output_bytes = bytearray()
        block_size = BLOCK_SIZE_BYTES
        iv_int = int.from_bytes(iv_bytes, 'big') # IV как число для инкремента

        for i in range(0, len(data_bytes), block_size):
            # Формируем блок счетчика
            counter_block_bytes = (iv_int + (i // block_size)).to_bytes(block_size, 'big')

            # Шифруем блок счетчика для получения гаммы
            gamma_block = cipher(counter_block_bytes, round_keys, Nr)

            # XOR гаммы с блоком данных
            data_chunk = data_bytes[i : i + block_size]
            gamma_part = gamma_block[:len(data_chunk)] # Обрезаем гамму

            result_chunk = bytes(a ^ b for a, b in zip(data_chunk, gamma_part))
            output_bytes.extend(result_chunk)

        return bytes(output_bytes)

    except Exception as e:
        print(f"Ошибка в aes_ctr_process: {e}")
        import traceback
        traceback.print_exc()
        return None

# --- Функции паддинга (могут быть нужны, если будем реализовывать другие режимы) ---
def pad_pkcs7(data: bytes, block_size: int = 16) -> bytes:
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad_pkcs7(data: bytes) -> bytes | None:
    if not data: return b''
    try:
        padding_len = data[-1]
        if padding_len == 0 or padding_len > len(data) or padding_len > 16 : raise ValueError("Invalid padding value")
        if not all(b == padding_len for b in data[-padding_len:]): raise ValueError("Invalid padding bytes")
        return data[:-padding_len]
    except (IndexError, ValueError) as e:
        print(f"Unpadding error: {e}")
        return None

# Пример использования
if __name__ == '__main__':
    # Тест AES-128
    key128_hex = "000102030405060708090a0b0c0d0e0f"
    iv_hex = "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"
    plain_hex = "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff" # 2 блока

    print("--- AES-128 CTR Test ---")
    key_bytes = hex_to_bytes(key128_hex)
    iv_bytes = hex_to_bytes(iv_hex)
    plain_bytes = hex_to_bytes(plain_hex)

    # Шифрование
    cipher_bytes = aes_ctr_process(plain_bytes, key_bytes, iv_bytes)
    if cipher_bytes:
        cipher_hex = bytes_to_hex(cipher_bytes)
        print(f"Plaintext (hex):  {plain_hex}")
        print(f"Key (hex):        {key128_hex}")
        print(f"IV (hex):         {iv_hex}")
        print(f"Ciphertext (hex): {cipher_hex}")
        # Ожидаемый результат для CTR с этими данными (пример из NIST SP 800-38A):
        # 874d6191b620e3261bef6864990db6ce9806f66b7970fdff8617187bb9fffdff
        expected_cipher_hex = "874d6191b620e3261bef6864990db6ce9806f66b7970fdff8617187bb9fffdff"
        print(f"Expected (hex):   {expected_cipher_hex}")
        print(f"Match:            {cipher_hex == expected_cipher_hex}")

    print("-" * 20)

    # Расшифрование
    if cipher_bytes:
        decrypted_bytes = aes_ctr_process(cipher_bytes, key_bytes, iv_bytes)
        if decrypted_bytes:
             decrypted_hex = bytes_to_hex(decrypted_bytes)
             print(f"Ciphertext (hex): {cipher_hex}")
             print(f"Key (hex):        {key128_hex}")
             print(f"IV (hex):         {iv_hex}")
             print(f"Decrypted (hex):  {decrypted_hex}")
             print(f"Original (hex):   {plain_hex}")
             print(f"Match:            {decrypted_hex == plain_hex}")