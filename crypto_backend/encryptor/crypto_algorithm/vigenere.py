# ASCII guide
# A = 65; a = 97
# Z = 90; z = 122

def convert_char_to_base26(character):

    if (character.islower()):
        return ord(character) - 97
    
    else :
        return ord(character) - 65

    return

# Convert a Base 26 to ASCII
def convert_base26_to_char(base26):
    #  Convert to Lowercase
    ascii_num = base26 + 97
    return chr(ascii_num)

# Get Inverse of Modulo
def get_inverse_of_m(m, divider):
    
    i = 1
    while(True):
        if ((m * i) % divider) == 1:
            return i 
        
        if (i == sys.maxsize):
            return -1

        i = i + 1

# Is char an alphabet
def is_alphabet(ch):

    if (ord(ch) >= 65 and ord(ch) <= 90):
        return True

    if (ord(ch) >= 97 and ord(ch) <= 122):
        return True

    return False


def print_squared_matrix(matrix):
    matrix_size = len(matrix)

    for i in range(matrix_size):
        for j in range(matrix_size):
            if (j == matrix_size - 1):
                print(matrix[j][i])
            else :
                print(matrix[j][i], end=' ')

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


