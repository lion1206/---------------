import copy


AES_SBOX = [
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

AES_INV_SBOX = [0] * 256
for i, val in enumerate(AES_SBOX):
    AES_INV_SBOX[val] = i


def aes_gmul(a, b):
    """Galois field multiplication of a and b in GF(2^8) with AES polynomial x^8 + x^4 + x^3 + x + 1 (0x11B)."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set:
            a ^= 0x1B
        b >>= 1
    return p


def aes_sub_bytes(state):
    """Applies the AES S-box to each byte of the state."""

    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_state[i][j] = AES_SBOX[state[i][j]]
    return new_state


def aes_inv_sub_bytes(state):
    """Applies the inverse AES S-box to each byte of the state."""
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_state[i][j] = AES_INV_SBOX[state[i][j]]
    return new_state


def aes_shift_rows(state):
    """Cyclically shifts the rows of the state."""

    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state


def aes_inv_shift_rows(state):
    """Cyclically shifts the rows of the state back."""

    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]
    return state


def aes_mix_columns(state):
    """Mixes the columns of the state using Galois field multiplication."""
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for j in range(4):
        s0, s1, s2, s3 = state[0][j], state[1][j], state[2][j], state[3][j]
        new_state[0][j] = aes_gmul(0x02, s0) ^ aes_gmul(0x03, s1) ^ s2 ^ s3
        new_state[1][j] = s0 ^ aes_gmul(0x02, s1) ^ aes_gmul(0x03, s2) ^ s3
        new_state[2][j] = s0 ^ s1 ^ aes_gmul(0x02, s2) ^ aes_gmul(0x03, s3)
        new_state[3][j] = aes_gmul(0x03, s0) ^ s1 ^ s2 ^ aes_gmul(0x02, s3)
    return new_state


def aes_inv_mix_columns(state):
    """Inverse Mixes the columns of the state using Galois field multiplication."""
    new_state = [[0 for _ in range(4)] for _ in range(4)]
    for j in range(4):
        s0, s1, s2, s3 = state[0][j], state[1][j], state[2][j], state[3][j]
        new_state[0][j] = aes_gmul(0x0e, s0) ^ aes_gmul(
            0x0b, s1) ^ aes_gmul(0x0d, s2) ^ aes_gmul(0x09, s3)
        new_state[1][j] = aes_gmul(0x09, s0) ^ aes_gmul(
            0x0e, s1) ^ aes_gmul(0x0b, s2) ^ aes_gmul(0x0d, s3)
        new_state[2][j] = aes_gmul(0x0d, s0) ^ aes_gmul(
            0x09, s1) ^ aes_gmul(0x0e, s2) ^ aes_gmul(0x0b, s3)
        new_state[3][j] = aes_gmul(0x0b, s0) ^ aes_gmul(
            0x0d, s1) ^ aes_gmul(0x09, s2) ^ aes_gmul(0x0e, s3)
    return new_state


def aes_add_round_key(state, round_keys, round_num):
    """Adds the round key to the state using XOR."""

    Nb = 4
    key_word_start_index = round_num * Nb
    for j in range(Nb):
        word_index = key_word_start_index + j
        for i in range(4):
            state[i][j] ^= round_keys[word_index][i]
    return state


def aes_key_expansion(key):
    """Expands the AES key (only supports 128-bit key)."""
    Nk = 4
    Nb = 4
    Nr = 10

    Rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    w = [[0 for _ in range(4)] for _ in range(Nb * (Nr + 1))]

    for i in range(Nk):
        for j in range(4):
            w[i][j] = key[i * 4 + j]

    for i in range(Nk, Nb * (Nr + 1)):
        temp = w[i - 1][:]
        if i % Nk == 0:

            temp = temp[1:] + temp[:1]

            for j in range(4):
                temp[j] = AES_SBOX[temp[j]]

            temp[0] = temp[0] ^ Rcon[i // Nk]

        for j in range(4):
            w[i][j] = w[i - Nk][j] ^ temp[j]

    return w


def format_state_to_hex(state):
    """Converts the 4x4 state matrix into a FIPS-style hex string (column-major linear)."""
    return "".join(f"{state[i][j]:02x}" for j in range(4) for i in range(4))


def format_round_key_to_hex(round_keys, round_num):
    """Formats the 16-byte round key for a given round into a hex string."""
    Nb = 4
    key_word_start_index = round_num * Nb
    hex_string = ""
    for j in range(Nb):
        word_index = key_word_start_index + j
        if word_index < len(round_keys):

            for byte_val in round_keys[word_index]:
                hex_string += f"{byte_val:02x}"
        else:
            hex_string += "???????? "
    return hex_string.strip()


def aes_encrypt_detailed(block, key):
    """
    Performs AES-128 encryption and prints intermediate states in FIPS B.1 format.
    Assumes block and key are 16-byte 'bytes' objects.
    Returns the 16-byte ciphertext as 'bytes'.
    """
    Nk = 4
    Nr = 10
    Nb = 4

    state = [[0 for _ in range(Nb)] for _ in range(4)]
    for r in range(4):
        for c in range(Nb):
            state[r][c] = block[r + 4 * c]

    round_keys = aes_key_expansion(key)

    print(f"В.1. AES-128 (Nk = {Nk}, Nr = {Nr})")
    print(f"открытый текст: {block.hex()}")
    print(f"ключ: {key.hex()}")
    print(f"Процедура шифрования (раунд r обозначается «round[r].»):")
    print(f"round[ 0].input {format_state_to_hex(state)}")
    print(f"round[ 0].k_sch {format_round_key_to_hex(round_keys, 0)}")

    state = aes_add_round_key(state, round_keys, 0)

    for round_num in range(1, Nr):
        print(f"round[ {round_num}].start {format_state_to_hex(state)}")
        state = aes_sub_bytes(state)
        print(f"round[ {round_num}].s_box {format_state_to_hex(state)}")
        state_after_sbox = copy.deepcopy(state)
        state_after_shift = aes_shift_rows(state_after_sbox)
        print(
            f"round[ {round_num}].s_row {format_state_to_hex(state_after_shift)}")
        state_after_mix = aes_mix_columns(state_after_shift)
        print(
            f"round[ {round_num}].m_col {format_state_to_hex(state_after_mix)}")
        print(
            f"round[ {round_num}].k_sch {format_round_key_to_hex(round_keys, round_num)}")

        state = aes_add_round_key(state_after_mix, round_keys, round_num)

    print(f"round[{Nr}].start {format_state_to_hex(state)}")
    state = aes_sub_bytes(state)
    print(f"round[{Nr}].s_box {format_state_to_hex(state)}")
    state_after_sbox = copy.deepcopy(state)
    state_after_shift = aes_shift_rows(state_after_sbox)
    print(f"round[{Nr}].s_row {format_state_to_hex(state_after_shift)}")

    print(f"round[{Nr}].k_sch {format_round_key_to_hex(round_keys, Nr)}")

    state = aes_add_round_key(state_after_shift, round_keys, Nr)

    output_block = bytearray(Nb * 4)
    for r in range(4):
        for c in range(Nb):
            output_block[r + 4 * c] = state[r][c]

    print(f"round[{Nr}].output {output_block.hex()}")

    return bytes(output_block)


def aes_decrypt_detailed(block, key):
    """
    Performs AES-128 decryption and prints intermediate states.
    Assumes block and key are 16-byte 'bytes' objects.
    Returns the 16-byte plaintext as 'bytes'.
    """
    Nk = 4
    Nr = 10
    Nb = 4

    state = [[0 for _ in range(Nb)] for _ in range(4)]
    for r in range(4):
        for c in range(Nb):
            state[r][c] = block[r + 4 * c]

    round_keys = aes_key_expansion(key)

    print(f"\nAES-128 Decryption (Nk = {Nk}, Nr = {Nr})")
    print(f"шифртекст: {block.hex()}")
    print(f"ключ: {key.hex()}")
    print(f"Процедура расшифрования:")
    print(f"round[ 0].input {format_state_to_hex(state)}")
    print(f"round[ 0].k_sch {format_round_key_to_hex(round_keys, Nr)}")

    state = aes_add_round_key(state, round_keys, Nr)

    for round_num in range(Nr - 1, 0, -1):
        print(f"round[{Nr - round_num}].start {format_state_to_hex(state)}")
        state = aes_inv_shift_rows(state)
        print(f"round[{Nr - round_num}].s_row {format_state_to_hex(state)}")
        state = aes_inv_sub_bytes(state)
        print(f"round[{Nr - round_num}].s_box {format_state_to_hex(state)}")
        print(
            f"round[{Nr - round_num}].k_sch {format_round_key_to_hex(round_keys, round_num)}")
        state = aes_add_round_key(state, round_keys, round_num)
        print(
            f"round[{Nr - round_num}].a_key {format_state_to_hex(state)}")
        state = aes_inv_mix_columns(state)
        print(
            f"round[{Nr - round_num}].m_col {format_state_to_hex(state)}")

    print(f"round[{Nr}].start {format_state_to_hex(state)}")
    state = aes_inv_shift_rows(state)
    print(f"round[{Nr}].s_row {format_state_to_hex(state)}")
    state = aes_inv_sub_bytes(state)
    print(f"round[{Nr}].s_box {format_state_to_hex(state)}")
    print(f"round[{Nr}].k_sch {format_round_key_to_hex(round_keys, 0)}")

    state = aes_add_round_key(state, round_keys, 0)

    output_block = bytearray(Nb * 4)
    for r in range(4):
        for c in range(Nb):
            output_block[r + 4 * c] = state[r][c]

    print(f"round[{Nr}].output {output_block.hex()}")

    return bytes(output_block)


while True:
    choice = input("Выберите режим работы (1 - шифрование, 2 - расшифрование, 3 - выход): ")
    if choice == "1":
        plaintext_hex = input("Введите сообщение (16 байт в hex): ")
        key_hex = input("Введите ключ (16 байт в hex): ")
    
        plaintext_bytes = bytes.fromhex(plaintext_hex)
        key_bytes = bytes.fromhex(key_hex)

        print("\n--- Запуск детального шифрования AES-128 ---")
        calculated_ciphertext_bytes = aes_encrypt_detailed(
            plaintext_bytes, key_bytes)
        print("--- Детальное шифрование завершено ---")

        print(f"\nПолученный шифртекст: {calculated_ciphertext_bytes.hex()}\n")

    elif choice == "2":
        ciphertext_hex = input("Введите шифртекст (16 байт в hex): ")
        key_hex = input("Введите ключ (16 байт в hex): ")
    
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        key_bytes = bytes.fromhex(key_hex)

        print("\n--- Запуск детального расшифрования AES-128 ---")
        calculated_plaintext_bytes = aes_decrypt_detailed(
            ciphertext_bytes, key_bytes)
        print("--- Детальное расшифрование завершено ---")

        print(f"\nПолученное сообщение: {calculated_plaintext_bytes.hex()}\n")

    elif choice == "3":
        break
    else:
        print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")