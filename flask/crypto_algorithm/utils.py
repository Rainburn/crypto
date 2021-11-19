# ASCII guide
# A = 65; a = 97
# Z = 90; z = 122

import sys
import random

# Convert a Char in Base 26, A = 0, Z = 25
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

# Convert a Char in Base 256
def convert_char_to_base256(character):
    return ord(character)
    
# Convert a Base 256 to ASCII
def convert_base256_to_char(base256):
    return chr(base256)

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

def create_full_vigenere_table():
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    alphabet_length = len(alphabet)
    table = [[0 for x in range(alphabet_length)] for y in range(alphabet_length)] 
    for i in range(alphabet_length):
        random_alphabet = alphabet[:]
        random.shuffle(random_alphabet)
        table[i] = random_alphabet
    return table


# XOR Bitwise on base 256
def xor_base256(a, b):

    a = '{:08b}'.format(a)
    b = '{:08b}'.format(b)

    length_a = len(a)
    length_b = len(b)

    # print(f"a : {a}")
    # print(f"b : {b}")

    result = ""

    for i in range(length_a):
        a_frag = int(a[i])
        b_frag = int(b[i])
        res_frag = (a_frag + b_frag) % 2

        result = result + str(res_frag)
    
    # print(f"result : {result}")

    return result


# String-byte to string convert
def stringbyte_to_string(string_byte):
    str_bin = int(string_byte,2)

    # print(str_bin)

    char_res = chr(str_bin)

    # print(char_res)

    return char_res


def gcd(a, b):
    min_number = a if (a < b) else b

    for j in range(min_number, 0, -1):
        if (a % j == 0 and b % j == 0):
            return j

def is_prime(n):
    if (n == 1):
        return False

    for j in range(n-1, 1, -1):
        if (n % j == 0):
            return False
    
    return True


def right_rotate(bin, n):

    len_bin = len(bin)

    curr_result = bin
    for i in range(n):
        last_char = curr_result[len_bin-1]
        curr_result = curr_result[0:len_bin-1]
        curr_result = last_char + curr_result

    return curr_result

def right_shift(bin, n):
    len_bin = len(bin)

    curr_result = bin
    for i in range(n):
        curr_result = curr_result[0:len_bin-1]
        curr_result = "0" + curr_result

    return curr_result

def not_binary(bin):
    res = ""
    for i in range(len(bin)):
        if (bin[i] == "1"):
            res += "0"
        else :
            res += "1"

    return res