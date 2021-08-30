from utils import *

# Affine Cipher

# With key m is a prime relative to n (total of alphabet)
# Possibilities of m : 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25

def affine_encrypt(plain, m, b):

    plain = plain.lower()

    plain_length = len(plain)

    cipher = ""

    for i in range(plain_length):
        p = convert_char_to_base26(plain[i])
        c_in_base26 = ((m * p) + b) % 26
        c = convert_base26_to_char(c_in_base26)
        cipher = cipher + c



    return cipher


def affine_decrypt(cipher, m, b):
    m_inv = get_inverse_of_m(m, 26)

    cipher = cipher.lower()
    cipher_length = len(cipher)

    plain = ""

    for i in range(cipher_length):
        c = convert_char_to_base26(cipher[i])
        p_in_base26 = ((c - b) * m_inv) % 26
        p = convert_base26_to_char(p_in_base26)
        plain = plain + p
    
    return plain