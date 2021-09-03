# ASCII guide
# A = 65; a = 97
# Z = 90; z = 122

import sys

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