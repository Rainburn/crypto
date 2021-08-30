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



def is_missing_char(ch, key_matrix):
    return False

def one_col_check(ch1, ch2, key_matrix):

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
                
                print("Found ch col at : ", ch1_col)

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

    ch1_next_row = (ch1_row + 1) % 5
    ch2_next_row = (ch2_row + 1) % 5

    ch1_next_char = key_matrix[ch1_col][ch1_next_row]
    ch2_next_char = key_matrix[ch1_col][ch2_next_row]

    return (ch1_next_char, ch2_next_char)


def one_row_check(ch1, ch2, key_matrix):

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

    ch1_next_col = (ch1_col + 1) % 5
    ch2_next_col = (ch2_col + 1) % 5

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


def playfair_encrypt():

    key = read_key()

    x = get_squared_chars("h", "r", key)
    print(x)

    return