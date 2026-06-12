import time

# =========================
# XOR FUNCTION
# =========================

def xor(a, b):
    return ''.join(
        '0' if x == y else '1'
        for x, y in zip(a, b)
    )

# =========================
# ROUND FUNCTION
# =========================

def round_function(right, key):
    return xor(right, key)

# =========================
# FEISTEL ENCRYPTION
# =========================

def feistel_encrypt(block, keys):

    left = block[:4]
    right = block[4:]

    for key in keys:

        temp = right

        f_output = round_function(right, key[:4])

        right = xor(left, f_output)

        left = temp

    return left + right

# =========================
# FEISTEL DECRYPTION
# =========================

def feistel_decrypt(block, keys):

    left = block[:4]
    right = block[4:]

    for key in reversed(keys):

        temp = left

        f_output = round_function(left, key[:4])

        left = xor(right, f_output)

        right = temp

    return left + right

# =========================
# ROUND KEYS (8 ROUNDS)
# =========================

keys = [
    "11110000",
    "11001100",
    "10101010",
    "00001111",
    "11111111",
    "00000000",
    "00110011",
    "01010101"
]

# =========================
# TEST
# =========================

plaintext = "10101010"

ciphertext = feistel_encrypt(plaintext, keys)

decrypted = feistel_decrypt(ciphertext, keys)

print("Plaintext :", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted :", decrypted)