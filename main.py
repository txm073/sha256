"""SHA-256 hash function implemented in pure Python"""

init_values = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
keys = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def binary(i, bits=32):
    py_binary = bin(i)[2:]
    return ("0" * (bits - len(py_binary))) + py_binary

def hex(i, bits=32):
    py_hex = __builtins__.hex(i)[2:]
    return ("0" * (bits // 4 - len(py_hex))) + py_hex

def get_blocks(bin_str):
    assert len(bin_str) % 512 == 0, "Binary string must be padded first"
    for i in range(0, len(bin_str), 512):
        yield bin_str[i:i+512]

def rotate(x, n, direction):
    assert direction in ("R", "L"), "Invalid direction"
    if isinstance(x, int):
        x = binary(x, 32)
    n = (abs(n) % 32) * (1 if direction == "L" else -1)
    return int(x[n:] + x[:n], base=2)

def transform(x, mode):
    assert mode in (0, 1), "Invalid mode"
    if mode == 0:
        return (rotate(x, 7, "R") ^ rotate(x, 18, "R")) ^ (x >> 3)
    return (rotate(x, 17, "R") ^ rotate(x, 19, "R")) ^ (x >> 10)

def ch(e, f, g):
    return (e & f) ^ ((~e) & g)

def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)

def sigma1(a):
    return rotate(a, 2, "R") ^ rotate(a, 13, "R") ^ rotate(a, 22, "R")

def sigma2(e):
    return rotate(e, 6, "R") ^ rotate(e, 11, "R") ^ rotate(e, 25, "R")

def add(*values):
    mod = 2 ** 32
    ans = values[0]
    for value in values[1:]:
        ans = (ans + value) % mod
    return ans

def next_word(w, i):
    return add(transform(w[i - 2], 1), w[i - 7], transform(w[i - 15], 0), w[i - 16])

def pad(data):
    bin_str = "".join([binary(ord(ch), 8) for ch in data]) + "1"
    length = len(bin_str) - 1
    while len(bin_str) % 512:
        bin_str += "0"
    return bin_str[:-8] + binary(length % (2 ** 8), 8)

def compress(block, iv):
    a, b, c, d, e, f, g, h = iv
    words = [int(block[i:i+32], base=2) for i in range(0, 512, 32)]
    for i in range(16, 64):
        words.append(next_word(words, i))
    for round_idx in range(64):
        t1 = add(h, sigma2(e), ch(e, f, g), keys[round_idx], words[round_idx])
        t2 = add(sigma1(a), maj(a, b, c))
        h, g, f = g, f, e
        e = add(d, t1)
        d, c, b = c, b, a
        a = add(t1, t2)
    return [add(i, j) for i, j in zip((a, b, c, d, e, f, g, h), iv)]

def sha256(data):
    states = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    bin_str = pad(data)
    for block in get_blocks(bin_str):
        states = compress(block, states)
    return "".join([hex(state, 32) for state in states])

if __name__ == "__main__":
    import hashlib

    msg = "Hello World!"#open(__file__).read()
    print(hashlib.sha256(msg.encode()).hexdigest())
    print(sha256(msg))
