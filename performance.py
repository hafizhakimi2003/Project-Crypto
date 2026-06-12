import time

# =========================
# RC4-LIKE STREAM CIPHER
# =========================

def ksa(key):
    key = [ord(c) for c in key]
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    return S

def prga(S, n):
    i = j = 0
    keystream = []

    for _ in range(n):
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        k = S[(S[i] + S[j]) % 256]
        keystream.append(k)

    return keystream

def rc4_encrypt(text, key):
    S = ksa(key)
    keystream = prga(S, len(text))

    cipher = []

    for i in range(len(text)):
        cipher.append(ord(text[i]) ^ keystream[i])

    return cipher

# =========================
# FEISTEL BLOCK CIPHER
# =========================

def xor(a, b):
    return ''.join(
        '0' if x == y else '1'
        for x, y in zip(a, b)
    )

def round_function(right, key):
    return xor(right, key)

def feistel_encrypt(block, keys):

    left = block[:4]
    right = block[4:]

    for key in keys:

        new_right = xor(
            left,
            round_function(right, key[:4])
        )

        left, right = right, new_right

    return left + right

# =========================
# RC4 PERFORMANCE TEST
# =========================

print("===== RC4 PERFORMANCE =====")

key = "secret"

text1 = "A" * 1024
text2 = "A" * 102400
text3 = "A" * 1048576

for text in [text1, text2, text3]:

    start = time.perf_counter()

    rc4_encrypt(text, key)

    end = time.perf_counter()

    print(
        f"Size: {len(text)} bytes | "
        f"Time: {end-start:.6f} seconds"
    )

# =========================
# FEISTEL PERFORMANCE TEST
# =========================

print("\n===== FEISTEL PERFORMANCE =====")

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

block1 = ["10101010"] * 128
block2 = ["10101010"] * 12800
block3 = ["10101010"] * 131072

for blocks in [block1, block2, block3]:

    start = time.perf_counter()

    for block in blocks:
        feistel_encrypt(block, keys)

    end = time.perf_counter()

    print(
        f"Blocks: {len(blocks)} | "
        f"Time: {end-start:.6f} seconds"
    )