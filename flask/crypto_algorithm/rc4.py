from utils import *

# RC4 Algorithm with Modification
# TODO: Make the modification


def ksa(key_in_string): # Key-Scheduling Algorithn

    internal_status = [i for i in range(256)]

    key_length = len(key_in_string)

    # Random the internal status
    j = 0
    for i in range(256):
        key_in_int = ord(key_in_string[i % key_length])

        j = (j + internal_status[i] + key_in_int) % 256

        # Swap
        temp = internal_status[j]
        internal_status[j] = internal_status[i]
        internal_status[i] = temp

    return internal_status


def ksa_modified(key_in_string):
    internal_status = [i for i in range(256)]

    key_length = len(key_in_string)

    # Random the internal status
    
    j = 0
    for i in range(256):
        key_in_int = ord(key_in_string[i % key_length])

        j = (j + internal_status[i] + key_in_int + key_length) % 256

        # Swap
        temp = internal_status[j]
        internal_status[j] = internal_status[i]
        internal_status[i] = temp

    return internal_status


def prga(text, internal_status): # Pseudo-random generation algorithm (PSGA)

    i = 0
    j = 0

    cipher = ""

    text_length = len(text)


    for idx in range(text_length):
        i = (i + 1) % 256
        j = (j + internal_status[i]) % 256

        # Swap
        temp = internal_status[j]
        internal_status[j] = internal_status[i]
        internal_status[i] = temp

        t = (internal_status[i] - internal_status[j]) % 256 # Little Modification here
        curr_keystream = internal_status[t]

        text_in_int = ord(text[idx])

        cipher_fragment = xor_base256(curr_keystream, text_in_int)

        # Convert cipher fragment to char
        cipher_fragment_str = stringbyte_to_string(cipher_fragment)

        # Merge fragment with result
        cipher = cipher + cipher_fragment_str

    return cipher


def rc4_encrypt(plain, key):

    initial_status = ksa(key)
    cipher = prga(plain, initial_status)

    return cipher


def rc4_decrypt(cipher, key):

    initial_status = ksa(key)
    plain = prga(cipher, initial_status)

    return plain


key = "SPATIAL DATABASE WITH MOVING OBJECT"
plain = "HOLY SLASH JEKI WHAT THE FUCK"

cipher = rc4_encrypt(plain, key)
plain_result = rc4_decrypt(cipher, key)

# internal_status = ksa(key)

# s = internal_status.copy()
# s2 = internal_status.copy()

# cipher = prga(plain, s)
# print()
# plain_result = prga(cipher, s2)
# print()



print(f"Initial Plain : {plain}")
print(f"Cipher : {cipher}")
print(f"Plain : {plain_result}")