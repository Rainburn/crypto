from utils import *

# Playfair Cipher

# Key is a 5x5 Matrix

def read_key():
    f = open("./examples/playfair/key.txt", "r")
    
    key_matrix = [[0 for i in range(5)] for x in range(5)]

    row_idx = 0
    for line in f:
        line_split = line.replace(" ", "")
        for col_idx in range(5):
            key_matrix[col_idx][row_idx] = line_split[col_idx].lower()
        
        row_idx = row_idx + 1

    return key_matrix


def get_missing_char(key_matrix):
    all_alphabet = [chr(i) for i in range(97,123)]

    for i in range(5):
        for j in range(5):
            all_alphabet.remove(key_matrix[i][j])

    return all_alphabet[0]

def is_missing_char(ch, key_matrix):
    return False

def one_col_check(ch1, ch2, key_matrix, encrypt_mode):

    ch1 = ch1.lower()
    ch2 = ch2.lower()

    ch1_col = -1
    ch1_row = -1

    # Get ch's Col
    for i in range(5):

        if (ch1_col != -1):
            break

        for j in range(5):
            if (ch1 == key_matrix[i][j]):
                ch1_col = i
                ch1_row = j

                break

    if (ch1_col == -1): # Missing Char
        return (-1, -1)

    # Check second char
    
    ch2_row = -1

    for i in range(5):
        if (ch2 == key_matrix[ch1_col][i]):
            ch2_row = i

    if (ch2_row == -1): # Not in the same col
        return (-1, -1)

    # Get Next char

    ch1_next_row = (ch1_row + 1) % 5 if (encrypt_mode) else (ch1_row - 1) % 5
    ch2_next_row = (ch2_row + 1) % 5 if (encrypt_mode) else (ch2_row - 1) % 5

    ch1_next_char = key_matrix[ch1_col][ch1_next_row]
    ch2_next_char = key_matrix[ch1_col][ch2_next_row]

    return (ch1_next_char, ch2_next_char)


def one_row_check(ch1, ch2, key_matrix, encrypt_mode):

    ch1 = ch1.lower()
    ch2 = ch2.lower()

    ch1_row = -1
    ch1_col = -1

    # Get ch's row
    for i in range(5):

        if (ch1_row != -1):
            break 

        for j in range(5):
            if (ch1 == key_matrix[i][j]):
                ch1_row = j
                ch1_col = i
                break
    
    if (ch1_row == -1): # Missing Char
        return (-1, -1)

    
    # Get Second Char
    ch2_col = -1

    for i in range(5):
        if (ch2 == key_matrix[i][ch1_row]):
            ch2_col = i
            break
    
    if (ch2_col == -1): # Not in the same row
        return (-1, -1)


    # Get Next char

    ch1_next_col = (ch1_col + 1) % 5 if (encrypt_mode) else (ch1_col - 1) % 5
    ch2_next_col = (ch2_col + 1) % 5 if (encrypt_mode) else (ch2_col - 1) % 5

    ch1_next_char = key_matrix[ch1_next_col][ch1_row]
    ch2_next_char = key_matrix[ch2_next_col][ch1_row]

    return (ch1_next_char, ch2_next_char)


def get_squared_chars(ch1, ch2, key_matrix):

    ch1 = ch1.lower()
    ch2 = ch2.lower()

    ch1_col = -1
    ch1_row = -1

    ch2_col = -1
    ch2_row = -1

    for i in range(5):
        for j in range(5):

            if (ch1 == key_matrix[i][j]):
                ch1_col = i
                ch1_row = j

            if (ch2 == key_matrix[i][j]):
                ch2_col = i
                ch2_row = j
            
    

    ch1_next = key_matrix[ch2_col][ch1_row]
    ch2_next = key_matrix[ch1_col][ch2_row]


    return (ch1_next, ch2_next)

def generate_key_matrix(key):

    # Remove all whitespaces
    key = key.lower()
    key = key.replace(" ", "")
    key_length = len(key)

    # Set unused char to 'j'
    missing_char = "j"

    all_alphabet = [chr(i) for i in range(97, 123)]
    all_alphabet.remove(missing_char)

    used_alphabet = []

    for i in range(key_length): 

        if (key[i] == missing_char):
            continue
        if (key[i] in used_alphabet):
            continue
        used_alphabet.append(key[i])
        all_alphabet.remove(key[i])

    used_alphabet = used_alphabet + all_alphabet

    # Convert to Matrix
    key_matrix = [[used_alphabet[j+i*5] for i in range(5)] for j in range(5)]

    return key_matrix


def plain_preps(plain):

    missing_char = 'j'
    misisng_char_replacement = 'i'
    subs_char = 'x'

    plain = plain.replace(missing_char, misisng_char_replacement)

    alphabet_only_plain = ""

    for i in range(len(plain)):
        if (is_alphabet(plain[i])):
            alphabet_only_plain = alphabet_only_plain + plain[i]

    
    plain = list(alphabet_only_plain)


    # Check pair with identical member
    plain_length = len(plain)
    current_idx = 0

    while (current_idx < plain_length):

        if (current_idx + 1 < plain_length):

            # Check whether the pair members are identical
            if (plain[current_idx] == plain[current_idx+1]):
                plain.insert(current_idx+1, subs_char)
                plain_length = plain_length + 1

                current_idx = current_idx + 2

            else :
                current_idx = current_idx + 2



        elif (current_idx + 1 >= plain_length):
            plain.append(subs_char)
            plain_length = plain_length + 1
            
            current_idx = current_idx + 2



    plain = ''.join(plain)

    plain_pairs = [plain[i:i+2] for i in range(0, len(plain), 2)]

    return plain_pairs


def playfair_encrypt(plain, key):

    # Key is a 5x5 Matrix
    key_matrix = generate_key_matrix(key)

    plain_pairs = plain_preps(plain)

    total_plain_pairs = len(plain_pairs)

    cipher = []


    for i in range(total_plain_pairs):
        ch1 = plain_pairs[i][0] 
        ch2 = plain_pairs[i][1]

        col_check_res = one_col_check(ch1, ch2, key_matrix, True)
        row_check_res = one_row_check(ch1, ch2, key_matrix, True)

        if (col_check_res != (-1,-1)):
            cipher.append(col_check_res[0] + col_check_res[1])
        
        elif (row_check_res != (-1,-1)):
            cipher.append(row_check_res[0] + row_check_res[1])
        
        else :
            square_res = get_squared_chars(ch1, ch2, key_matrix)
            cipher.append(square_res[0] + square_res[1])


    cipher_as_string = ''.join(cipher)

    return cipher_as_string

def playfair_decrypt(cipher, key):

    key_matrix = generate_key_matrix(key)

    cipher_length = len(cipher)

    cipher_pairs = [cipher[i:i+2] for i in range(0, cipher_length, 2)]

    plain = []

    print(cipher_pairs)

    for i in range(len(cipher_pairs)):
        ch1 = cipher_pairs[i][0]
        ch2 = cipher_pairs[i][1]

        col_check_res = one_col_check(ch1, ch2, key_matrix, False)
        row_check_res = one_row_check(ch1, ch2, key_matrix, False)

        if (col_check_res != (-1,-1)):
            plain.append(col_check_res[0] + col_check_res[1])

        elif (row_check_res != (-1,-1)):
            plain.append(row_check_res[0] + row_check_res[1])

        else :
            square_res = get_squared_chars(ch1, ch2, key_matrix)
            plain.append(square_res[0] + square_res[1])

    plain_as_string = ''.join(plain)

    plain_result = plain_as_string.replace("x", "")

    return plain_result