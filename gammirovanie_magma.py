from typing import List, Union
import struct

SBOX = [
    [1,  7, 14, 13, 0,  5,  8,  3,  4, 15, 10, 6,  9, 12, 11, 2],
    [8,  14, 2,  5,  6,  9,  1, 12, 15, 4,  11, 0, 13, 10, 3,  7],
    [5,  13, 15, 6,  9,  2, 12, 10, 11, 7,   8, 1,  4,  3, 14, 0],
    [7,  15, 5, 10,  8,  1,  6, 13,  0, 9,   3, 14, 11, 4,  2, 12],
    [12, 8,  2,  1, 13,  4, 15,  6,  7, 0,  10, 5,   3, 14, 9, 11],
    [11, 3,  5,  8,  2, 15, 10, 13, 14, 1,   7, 4,  12, 9,  6,  0],
    [6,  8,  2,  3,  9, 10,  5, 12,  1, 14,  4, 7,  11, 13, 0, 15],
    [12, 4,  6,  2, 10,  5, 11,  9, 14, 8,  13, 7,   0, 3, 15,  1]
]

def hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes."""
    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string must have even length")
    return bytes.fromhex(hex_str)

def bytes_to_hex(data: bytes) -> str:
    """Convert bytes to hex string."""
    return data.hex()

def t_transform(x: int) -> int:
    """Apply SBOX transformation."""
    result = 0
    for i in range(8):
        nib = (x >> (4 * i)) & 0xF
        sub = SBOX[7 - i][nib]
        result |= (sub << (4 * i))
    return result

def g_function(a: int, k: int) -> int:
    """G function for MAGMA."""
    sum_val = (a + k) & 0xFFFFFFFF
    t = t_transform(sum_val)
    return ((t << 11) | (t >> (32 - 11))) & 0xFFFFFFFF

def feistel_round(l: int, r: int, k: int) -> tuple[int, int]:
    """Single Feistel round."""
    return r, (l ^ g_function(r, k)) & 0xFFFFFFFF

def expand_key(key_hex: str) -> List[int]:
    """Expand 256-bit key into round keys."""
    if not len(key_hex) == 64 or not all(c in '0123456789abcdefABCDEF' for c in key_hex):
        raise ValueError("Key must be 64 hex characters")
    
    parts = []
    for i in range(8):
        w = key_hex[i * 8:(i + 1) * 8]
        parts.append(int(w, 16))
    
    round_keys = []
    for _ in range(3):
        round_keys.extend(parts)
    for j in range(7, -1, -1):
        round_keys.append(parts[j])
    
    return round_keys

def encrypt_block64(counter: int, round_keys: List[int]) -> int:
    """Encrypt a 64-bit block."""
    l = (counter >> 32) & 0xFFFFFFFF
    r = counter & 0xFFFFFFFF
    
    for i in range(32):
        l, r = feistel_round(l, r, round_keys[i])
    
    return (r << 32) | l

def ctr_encrypt_bytes(data: bytes, key_hex: str, iv_hex: str) -> bytes:
    """Encrypt/decrypt data using CTR mode."""
    if len(iv_hex) == 8:
        iv_full = iv_hex + "0" * 8
    elif len(iv_hex) == 16:
        iv_full = iv_hex
    else:
        raise ValueError("IV must be 8 or 16 hex characters")

    round_keys = expand_key(key_hex)
    ctr = int(iv_full, 16)
    output = bytearray()

    for pos in range(0, len(data), 8):
        length = min(8, len(data) - pos)
        gamma = encrypt_block64(ctr, round_keys)
        gamma_bytes = struct.pack('>Q', gamma)
        
        for i in range(length):
            output.append(data[pos + i] ^ gamma_bytes[i])
        
        ctr = (ctr + 1) & ((1 << 64) - 1)

    return bytes(output)

def gamma_encrypt(text: str, key_hex: str, iv_hex: str) -> str:
    """Encrypt text using MAGMA in CTR mode."""
    tokens = text.strip().split()
    is_hex_blocks = all(len(t) == 16 and all(c in '0123456789abcdefABCDEF' for c in t) for t in tokens)

    if is_hex_blocks:
        pt_bytes = hex_to_bytes(''.join(tokens))
        ct_bytes = ctr_encrypt_bytes(pt_bytes, key_hex, iv_hex)
        hex_str = bytes_to_hex(ct_bytes)
        return ' '.join(hex_str[i:i+16] for i in range(0, len(hex_str), 16))
    else:
        pt_bytes = text.encode('utf-8')
        ct_bytes = ctr_encrypt_bytes(pt_bytes, key_hex, iv_hex)
        return bytes_to_hex(ct_bytes)

def gamma_decrypt(text: str, key_hex: str, iv_hex: str) -> str:
    """Decrypt text using MAGMA in CTR mode."""
    tokens = text.strip().split()
    is_hex_blocks = all(len(t) == 16 and all(c in '0123456789abcdefABCDEF' for c in t) for t in tokens)

    if is_hex_blocks:
        ct_bytes = hex_to_bytes(''.join(tokens))
        pt_bytes = ctr_encrypt_bytes(ct_bytes, key_hex, iv_hex)
        hex_str = bytes_to_hex(pt_bytes)
        return ' '.join(hex_str[i:i+16] for i in range(0, len(hex_str), 16))
    else:
        ct_bytes = hex_to_bytes(text)
        pt_bytes = ctr_encrypt_bytes(ct_bytes, key_hex, iv_hex)
        return pt_bytes.decode('utf-8')

def main():
    try:
        text = input("Введите текст: ")
        key = input("Введите ключ: ")
        iv = input("Введите iv: ")

        encrypted = gamma_encrypt(text, key, iv)
        decrypted = gamma_decrypt(encrypted, key, iv)

        print("Зашифрованный текст:", encrypted)
        print("Расшифрованный текст:", decrypted)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
## Введите текст: 92def06b3c130a59 db54c704f8189d20 4a98fb2e67a8024c 8912409b17b57e41
## Введите ключ:  ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff
## Выходные данные: 4e98110c97b7b93c 3e250d93d6e85d69 136d868807b2dbef 568eb680ab52a12d
## IV: 12345678