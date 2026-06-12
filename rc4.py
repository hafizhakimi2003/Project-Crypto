import time

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


# PERFORMANCE TEST

text1 = "A" * 1024        # 1KB
text2 = "A" * 102400      # 100KB
text3 = "A" * 1048576     # 1MB

key = "secret"

for text in [text1, text2, text3]:

    start = time.perf_counter()

    encrypted = rc4_encrypt(text, key)

    end = time.perf_counter()

    print(f"Size: {len(text)} bytes")
    print(f"Time: {end - start:.6f} seconds")
    print()