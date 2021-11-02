from .utils import *

# RC4 Algorithm with Modification
# TODO: Make the modification


def read_file_binary(filename):
    f = open(filename, "rb")

    read_bytes_string = ""

    byte = f.read(1)
    size = 0
    while (byte):
        read_bytes_string = read_bytes_string + chr(ord(byte))

        byte = f.read(1)
        size = size + 1

    print(f"Size : {size}")
    print(f"Read bytes length : {len(read_bytes_string)}")

    f.close()

    return read_bytes_string



def save_file_binary(filename, content):

    content_as_bytearray = []
    for byte in content:
        content_as_bytearray.append(ord(byte)) 

    print(f"Content as byte length : {len(content_as_bytearray)}")

    content_as_bytearray = bytearray(content_as_bytearray)

    f = open(filename, "wb")
    f.write(content_as_bytearray)

    f.close()


def read_file_text(filename):
    f = open(filename, "r")

    lines = f.readlines()

    content = ""

    for line in lines:
        for char in line:
            content = content + char

    f.close()

    return content


def save_file_text(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()


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


def rc4_encrypt(plain, key, from_http_req=True):

    initial_status = ksa(key)
    cipher = prga(plain, initial_status)

    if (not(from_http_req)):
        return cipher
    
    cipher_ord_array = []
    
    for c in cipher:
        cipher_ord_array.append(ord(c))
    
    return cipher_ord_array


def rc4_decrypt(cipher, key, from_http_req=True):

    initial_status = ksa(key)
    plain = prga(cipher, initial_status)

    if (not(from_http_req)):
        return plain

    plain_ord_array = []
    for p in plain:
        plain_ord_array.append(ord(p))

    return plain_ord_array

# Example with Hardcoded / Input text

key = "AKEY"
plain = "SOMEPLAINTEXT"

cipher = rc4_encrypt(plain, key, False)
plain_result = rc4_decrypt(cipher, key, False)

print(f"Initial Plain : {plain}")
print(f"Cipher : {cipher}")
print(f"Plain : {plain_result}")


# Example with Binary file

# key = "INI GAMBAR DARI PPT"
# plain = read_file_binary("test.png")
# cipher = rc4_encrypt(plain, key)
# save_file_binary("cipher_test.png", cipher)

# plain_result = rc4_decrypt(cipher, key)
# save_file_binary("plain_result.png", plain_result)


# same = True
# for i in range(len(plain)):
#     if (plain[i] != plain_result[i]):
#         same = False
#         print("Not Same")
#         break

# if (same):
#     print("Same")


# Example with Text file
# plain = read_file_text("plain.txt")
# print(plain)
# save_file_text("plain2.txt", plain)