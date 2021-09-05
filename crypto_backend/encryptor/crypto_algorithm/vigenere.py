# ASCII guide
# A = 65; a = 97
# Z = 90; z = 122
import utils
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
def full_vigenere_encrypt(plain,key):
    
    # Create custom table for Full Vigenere
    table=create_full_vigenere_table()
    
    # Convert All to Lower
    plain = plain.lower()

    plain_length = len(plain)
    key_length = len(key)

    cipher = ""
    key_loop = key

    # Key is shorter than plain
    if (key_length < plain_length):
        
        for i in range(plain_length-key_length):
            loop_idx = i % key_length
            key_loop = key_loop + key[loop_idx]

    # Encrypting
    for i in range(plain_length):
        p = convert_char_to_base26(plain[i]) % 26
        k = convert_char_to_base26(key_loop[i]) % 26
        cipher = cipher + table[k][p]
    
    return [cipher,table]
    
def full_vigenere_decrypt(cipher,key,table):
    cipher = cipher.lower()

    cipher_length = len(cipher)
    key_length = len(key)

    plain = ""
    key_loop = key

    # Key is shorter than plain
    if (key_length < cipher_length):
        
        for i in range(cipher_length-key_length):
            loop_idx = i % key_length
            key_loop = key_loop + key[loop_idx]

    # Decrypting
    for i in range(cipher_length):
        k = convert_char_to_base26(key_loop[i]) % 26
        c = table[k].index(cipher[i])
        plain = plain + convert_base26_to_char(c)

    return plain

# Auto-Key Vigenere Cipher
def auto_key_encrypt(plain,key):
    
    plain = plain.lower()
    
    plain_length = len(plain)
    key_length = len(key)

    cipher = ""
    key_loop = key
    
    #If key is shorter than plain text, concatenate with plaintext
    if(key_length<plain_length):
        for i in range(plain_length-key_length):
            key_loop = key_loop + plain[i]

    #Encryption
    for i in range(plain_length):
        p = convert_char_to_base26(plain[i])
        k = convert_char_to_base26(key_loop[i])
        c_in_ascii = (p + k) % 26
        c = convert_base26_to_char(c_in_ascii)
        cipher = cipher + c

    return cipher
    
def auto_key_decrypt(cipher,key):
    cipher = cipher.lower()

    cipher_length = len(cipher)
    key_length = len(key)

    plain = ""
    key_loop = key
    
     #If key is shorter than plain text, concatenate with decrypted key
    if(key_length<cipher_length):
        for i in range(cipher_length-key_length):
            c = convert_char_to_base26(cipher[i])
            k = convert_char_to_base26(key_loop[i])
            p_in_ascii = (c - k) % 26
            key_loop = key_loop + convert_base26_to_char(p_in_ascii)
    
    #Decryption
    for i in range(cipher_length):
        c = convert_char_to_base26(cipher[i])
        k = convert_char_to_base26(key_loop[i])
        p_in_ascii = (c - k) % 26
        p = convert_base26_to_char(p_in_ascii)
        plain = plain + p

    return plain

def extended_vigenere_encrypt(plain,key):

    plain_length = len(plain)
    key_length = len(key)

    cipher = ""
    key_loop = key

    # Key is shorter than plain
    if (key_length < plain_length):
        
        for i in range(plain_length-key_length):
            loop_idx = i % key_length
            key_loop = key_loop + key[loop_idx]

    print(key_loop)
    # Encrypting
    for i in range(plain_length):
        p = convert_char_to_base256(plain[i])
        k = convert_char_to_base256(key_loop[i])
        c_in_ascii = (p + k) % 256
        c = convert_base256_to_char(c_in_ascii)
        cipher = cipher + c

    return cipher

def extended_vigenere_decrypt(cipher, key):

    cipher_length = len(cipher)
    key_length = len(key)

    plain = ""
    key_loop = key

    # Key is shorter than plain
    if (key_length < cipher_length):

        for i in range(cipher_length-key_length):
            loop_idx = i % key_length
            key_loop = key_loop + key[loop_idx]


    # Decrypting
    for i in range(cipher_length):
        c = convert_char_to_base256(cipher[i])
        k = convert_char_to_base256(key_loop[i])
        p_in_ascii = (c - k) % 256
        p = convert_base256_to_char(p_in_ascii)
        
        plain = plain + p

    return plain
