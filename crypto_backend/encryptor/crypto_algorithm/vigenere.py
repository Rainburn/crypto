# ASCII guide
# A = 65; a = 97
# Z = 90; z = 122

from .utils import *

# Vigenere Cipher Basic

def vigenere_encrypt(plain, key):

    # Convert All to Lower
    plain = plain.lower()

    plain_length = len(plain)
    key_length = len(key)

    cipher = ""

    # Key is shorter than plain
    if (key_length < plain_length):
        
        # Repeat the key
        key_loop = ""
        
        for i in range(plain_length):
            loop_idx = i % key_length
            key_loop = key_loop + key[loop_idx]


        # Encrypting

        for i in range(plain_length):
            p = convert_char_to_base26(plain[i])
            k = convert_char_to_base26(key_loop[i])
            c_in_ascii = (p + k) % 26
            c = convert_base26_to_char(c_in_ascii)
            cipher = cipher + c

        return cipher

    else: # Key is equal or longer than plain

        for i in range(plain_length):
            p = convert_char_to_base26(plain[i])
            k = convert_char_to_base26(key[i])
            c_in_ascii = (p + k) % 26
            c = convert_base26_to_char(c_in_ascii)
            cipher = cipher + c

        return cipher.upper()
        


def vigenere_decrypt(cipher, key):

    # Convert All to Lower
    cipher = cipher.lower()

    cipher_length = len(cipher)
    key_length = len(key)

    plain = ""

    # Key is shorter than plain
    if (key_length < cipher_length):
        
        # Repeat the key
        key_loop = ""
        
        for i in range(cipher_length):
            loop_idx = i % key_length
            key_loop = key_loop + key[loop_idx]


        # Encrypting

        for i in range(cipher_length):
            c = convert_char_to_base26(cipher[i])
            k = convert_char_to_base26(key_loop[i])
            p_in_ascii = (c - k) % 26
            p = convert_base26_to_char(p_in_ascii)
            plain = plain + p

        return plain

    else: # Key is equal or longer than plain

        for i in range(cipher_length):
            c = convert_char_to_base26(cipher[i])
            k = convert_char_to_base26(key[i])
            p_in_ascii = (c - k) % 26
            p = convert_base26_to_char(p_in_ascii)
            plain = plain + p

        return plain


# Full Vigenere Cipher


# Auto-Key Vigenere Cipher
