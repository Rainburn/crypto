from .utils import *
import random

def l_function(x, n):
    return int((x - 1)/n)


def paillier_create_keys(p, q, g):
    # P and Q must be prime numbers
    if ((not is_prime(p)) or (not is_prime(q))):
        print("P or Q is not prime")
        return

    # Validate P and Q, pq and (p - 1)(q - 1) must be prime relative to each other
    if (gcd(p * q, (p-1) * (q-1)) != 1):
        print("PQ and (P-1)(Q-1) are not prime relatives")
        return

    n = p * q
    lambd = int((p-1) * (q-1) / gcd(p-1, q-1)) # This must be lcm(p - 1, q - 1)

    # Pick g where g < n^2
    if (g >= n * n):
        print("g is not smaller than n^2")
        return

    x = pow(g, lambd) % (n * n)
    y = l_function(x, n)

    i = 0
    k_found = False
    k = -1
    while (not k_found):
        if ((i * n + 1) % y == 0):
            k = i
            k_found = True
            break
            
        i += 1

    u = int((k * n + 1) / y)

    keys = {
        "public": (g, n),
        "private": (lambd, u)
    }
    
    print(keys)

    return keys


def encrypt_message(plain, g, n):

    # let m be the message to be encrypted
    # with 0 <= m < n
    # Validate m here as char
    
    m = ord(plain)
    
    # if (type(plain) is str):
    #     m = convert_char_to_base26(plain)

    # else :
    #     m = plain

    if (m >= n):
        print("M is bigger or same with N")
        return 
    
    # r is a random number between 0 <= r < n, and gcd(r, n) = 1
    # Randomize and validate R here

    r_found = False
    r = -1
    while(not r_found):
        r = random.randrange(0, n-1)

        if (gcd(r,n) == 1):
            r_found = True
            break
    
    # Encrypt m to c 

    c = (pow(g, m) * pow(r, n)) % (n * n)

    print(f"r : {r}")
    print(f"C : {c}")

    return c


def decrypt_message(cipher, n, lambd, u):
    # Cipher is in LONGINT Form

    above_par = pow(cipher, lambd) % (n * n)

    m = (l_function(above_par, n) * u) % (n)

    print(f"m : {m}")
    return m


def paillier_encrypt(plain, g, n):

    cipher_blocks = []

    for i in range(len(plain)):
        m = plain[i]
        c = encrypt_message(m, g, n)
        cipher_blocks.append(str(c))

    return " ".join(cipher_blocks)


def paillier_decrypt(cipher_string, n, lambd, u):

    cipher_blocks = cipher_string.split(" ")
    plain_blocks = []

    for i in range(len(cipher_blocks)):
        c = int(cipher_blocks[i])
        m = decrypt_message(c, n, lambd, u)
        plain_blocks.append(chr(m))

    return "".join(plain_blocks)


# p = 1019
# q = 1039
# n = p * q
# keys = create_keys(p, q, 5652)
# print(keys)

# # Private Keys

# # lamb = keys['private'][0]
# # u = keys['private'][1]

# plain = "RafiA"
# c = paillier_encrypt(plain, 5652, n)
# m = paillier_decrypt(c, n, lamb, u)
# print(f"Cipher : {c}")
# print(f"Plain res : {m}")
