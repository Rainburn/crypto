from utils import *


def create_keys(p, q, e):
    # P and Q must be prime numbers and must be big enough

    if (p * q - 1 <= 127127):
        print("Use Bigger P and Q")
        return

    # Validate P and Q here
    if ((not is_prime(p)) or (not is_prime(q))):
        print("P or Q is not prime")
        return

    n = p * q
    q_n = (p - 1) * (q - 1)

    # Pick e, e must be prime relative to q_n
    # Validate e here
    if (gcd(e, q_n) != 1):
        print("e must be prime relative to q_n")
        return

    i = 0
    k_found = False
    k = -1
    while (not k_found):
        if ((i * q_n + 1) % e == 0):
            k = i
            k_found = True
            break
        i += 1

    d = int((k * q_n + 1) / e)

    keys = {
        "public": (e, n),
        "private": (d, n)
    }

    return keys


def encrypt_message(plain, e, n):
    plain = plain.strip()
    plain = plain.lower()

    plain_blocks = []

    block_size = 2 # Size in Alphabet
    block_message = ""

    counter = 0
    for i in range(len(plain)):
        
        if (counter == block_size):
            plain_blocks.append(block_message)
            block_message = ""
            counter = 0


        # block_message += base26
        c = str(ord(plain[i]))

        if (len(c) % 3 == 2):
            c = "0" + c
        elif (len(c) % 3 == 1):
            c = "00" + c

        block_message += c
        counter += 1   

        if (i == len(plain) - 1):
            plain_blocks.append(block_message)
            break     
    

    # Encrypt here
    cipher_blocks = []

    for block in plain_blocks:
        cipher_block = pow(int(block), e) % n
        cipher_blocks.append(cipher_block)

    return cipher_blocks

def rsa_encrypt(plain, e, n):

    block_size = 2 # Size in alphabet
    cipher_blocks = encrypt_message(plain, e, n)

    

    for i in range(len(cipher_blocks)):
        cipher_blocks[i] = str(cipher_blocks[i])


    return " ".join(cipher_blocks)


def rsa_decrypt(cipher_string, d, n):
    plain = ""
    cipher_blocks = cipher_string.split(" ")

    block = ""
    counter = 0

    # Decrypting process here
    plain_blocks = []
    for i in range(len(cipher_blocks)):
        block = cipher_blocks[i]
        m = pow(int(block), d) % n
        str_m = str(m)

        if (len(str_m) < 6 and i != len(cipher_blocks) - 1):
            additional_zeros = ""
            for j in range(6 - len(str_m)):
                additional_zeros = "0" + additional_zeros

            str_m = additional_zeros + str_m

        if (len(str_m) % 3 == 1 and i == len(cipher_blocks) - 1):
            str_m = "00" + str_m

        elif (len(str_m) % 3 == 2 and i == len(cipher_blocks) - 1):
            str_m = "0" + str_m

        plain_blocks.append(str_m)

    # Merge plain blocks into plain string
    plain_string = ""
    for block in plain_blocks:
        total_alphabet = int(len(block) / 3)  
        for i in range(total_alphabet):
            ordinal = block[i*3:i*3+3]
            plain_string += chr(int(ordinal))


    print(plain_string)
    return plain_string


keys = create_keys(1019, 1039, 79)
e = keys['public'][0]
n = keys['public'][1]
d = keys['private'][0]

cipher_string = rsa_encrypt("TucilKriptoRSA", e, n)
plain_res = rsa_decrypt(cipher_string, d, n)

print(f"d : {d}")
print(f"Cipher string : {cipher_string}")
print(f"Plain result : {plain_res}")