def binary(i, bits=8):
    py_binary = bin(i)[2:]
    return ("0" * (bits - len(py_binary))) + py_binary

def get_blocks(bin_str):
    assert len(bin_str) % 512 == 0, "Binary string must be padded first"
    for i in range(0, len(bin_str), 512):
        yield bin_str[i:i+512]

def get_primes(n, max=None):
    nums = list(range(2, n + 1, 1))
    marker = [0] * n
    primes = []
    for index, num in enumerate(nums):
        if marker[index] == 0:
            primes.append(num)
            if len(primes) == max:
                return primes
            for j in range(index + num, len(nums), num):
                marker[j] = 1
    return primes

def rotl(x, d):
    return (x << d) | (x >> (32 - d))
 
def rotr(x, d):
    return (x >> d) | (x << (32 - d)) 

def transform(x, mode=0):
    assert mode in (0, 1), "Invalid mode"
    return rotr(x, 17 if mode else 7) ^ rotr(x, 19 if mode else 18) ^ (x >> 10 if mode else 3)

def next_word(w, i):
    return transform(w[i - 2], 1) + w[i - 7] + transform(w[i - 15], 0) + w[i - 16]

def encode(data):
    init_values = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    print(init_values)
    print([int((p ** (1 / 2) % 1) * 16 ** 8) for p in get_primes(20, max=8)])
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
    bin_str = "".join([binary(ord(ch)) for ch in data]) + "1"
    length = len(bin_str) - 1
    while len(bin_str) % 512:
        bin_str += "0"
    bin_str = bin_str[:-8] + binary(length % (2 ** 8))
    for block in get_blocks(bin_str):
        words = [block[i:i+32] for i in range(0, 512, 32)]
        print("\n".join(words))

encode("portsmouth")
print(bin(rotr(int("01110011011011010110111101110101", base=2), 7)))