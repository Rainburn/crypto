import os
import math
from utils import *

def sha256(lines, original_size):

    # f = open(filename, "r")

    # lines = f.readlines()

    # f.close()

    total_char = 0
    # original_size = os.stat(filename).st_size

    bins_string = ""

    # Step 1 : Read Files and Convert to Binary

    for line in lines:
        for char in line:
            # For RB
            # octa = int(oct(char), 8) 
            
            # For R
            ordinal = ord(char)

            char_bin = '{:08b}'.format(ordinal)
            total_char += 1
            bins_string += char_bin
            bins_string += " "


    # Add a single 1 below
    total_char += 1
    bins_string += "10000000"
    bins_string += " "

    total_zero_append = 448 - ((total_char * 8) % 512)

    print("Zero Appends : ", total_zero_append)

    # Append Zero
    for i in range(1, total_zero_append + 1):
        bins_string += "0"
        # size += 1

        if (i % 8 == 0):
            bins_string += " "

    # Append filesize as last 64 bit
    original_size_bin = '{:064b}'.format(original_size * 8)
    original_size_bin_split = ""
    for i in range(1, 65):
        original_size_bin_split += original_size_bin[i-1]
        if (i % 8 == 0):
            original_size_bin_split += " "

    bins_string += original_size_bin_split
    print("Original size in binary : ", original_size_bin_split)

    # Step 2 : Initialize Hash Values (h). Based on first 32 bits of square root of first 8 primes
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19


    # Step 3 : Initialize Round Constant. Based on first 32 bits of cube root of first 64 primes

    k_string = [None for i in range(8)]
    k_string[0] = "0x428a2f98 0x71374491 0xb5c0fbcf 0xe9b5dba5 0x3956c25b 0x59f111f1 0x923f82a4 0xab1c5ed5"
    k_string[1] = "0xd807aa98 0x12835b01 0x243185be 0x550c7dc3 0x72be5d74 0x80deb1fe 0x9bdc06a7 0xc19bf174"
    k_string[2] = "0xe49b69c1 0xefbe4786 0x0fc19dc6 0x240ca1cc 0x2de92c6f 0x4a7484aa 0x5cb0a9dc 0x76f988da"
    k_string[3] = "0x983e5152 0xa831c66d 0xb00327c8 0xbf597fc7 0xc6e00bf3 0xd5a79147 0x06ca6351 0x14292967"
    k_string[4] = "0x27b70a85 0x2e1b2138 0x4d2c6dfc 0x53380d13 0x650a7354 0x766a0abb 0x81c2c92e 0x92722c85"
    k_string[5] = "0xa2bfe8a1 0xa81a664b 0xc24b8b70 0xc76c51a3 0xd192e819 0xd6990624 0xf40e3585 0x106aa070"
    k_string[6] = "0x19a4c116 0x1e376c08 0x2748774c 0x34b0bcb5 0x391c0cb3 0x4ed8aa4a 0x5b9cca4f 0x682e6ff3"
    k_string[7] = "0x748f82ee 0x78a5636f 0x84c87814 0x8cc70208 0x90befffa 0xa4506ceb 0xbef9a3f7 0xc67178f2"

    k_constant = []

    for i in range(8):
        curr_array = k_string[i].split()
        for j in range(len(curr_array)):
            k_constant.append("{:032b}".format(int(curr_array[j], 16)))
            
    # Step 4 : Chunk Loop

    w = []

    bins_array = bins_string.split()
    # print("Bins arr length : ", len(bins_array))

    # Copy step 1 result into W
    partial_32 = ""
    for i in range(1, len(bins_array) + 1):
        partial_32 += bins_array[i-1]

        if (i % 4 == 0):
            w.append(partial_32)
            partial_32 = ""

    # Add other words until w is 64 length
    total_word_append = 64 - len(w)
    len_w_before_append = len(w)
    zero_row_32 = "00000000000000000000000000000000"

    for i in range(total_word_append):
        w.append(zero_row_32)


    # Modify zero-ed indexes at the end of the array using these following algorithm :
    # NOTE : STILL DON'T KNOW WHETHER W[i - 15] or W[i - len_w_before_append-1]
    for i in range(len_w_before_append, 64):
        # s0
        minus_idx = 15
        # minus_idx = len_w_before_append - 1
        p1 = right_rotate(w[i - minus_idx], 7)
        p2 = right_rotate(w[i - minus_idx], 18)
        p3 = right_shift(w[i - minus_idx], 3)
        s0 = "{:032b}".format(int(p1,2) ^ int(p2,2) ^ int(p3,2))

        # s1
        p1 = right_rotate(w[i - 2], 17)
        p2 = right_rotate(w[i - 2], 19)
        p3 = right_shift(w[i - 2], 10)
        s1 = "{:032b}".format(int(p1,2) ^ int(p2,2) ^ int(p3,2))

        # w[i]
        w_curr = int((int(w[i-16], 2) + int(s0, 2) + int(w[i-7], 2) + int(s1, 2)) % math.pow(2, 32))
        w[i] = "{:032b}".format(w_curr)


    # Step 6 : Compression
    a = "{:032b}".format(h0)
    b = "{:032b}".format(h1)
    c = "{:032b}".format(h2)
    d = "{:032b}".format(h3)
    e = "{:032b}".format(h4)
    f = "{:032b}".format(h5)
    g = "{:032b}".format(h6)
    h = "{:032b}".format(h7)

    # Doing compression loop
    for i in range(64):
        # s1
        p1 = right_rotate(e, 6)
        p2 = right_rotate(e, 11)
        p3 = right_rotate(e, 25)
        s1 = "{:032b}".format(int(p1,2) ^ int(p2,2) ^ int(p3,2))

        # ch
        p1 = int(e, 2) & int(f, 2)
        p2 = int(not_binary(e), 2) & int(g, 2)
        ch_int = p1 ^ p2
        ch = "{:032b}".format(ch_int)

        # temp1
        temp1 = int((int(h, 2) + int(s1, 2) + int(ch, 2) + int(k_constant[i], 2) + int(w[i], 2)) % math.pow(2, 32))
        temp1 = "{:032b}".format(temp1)

        # s0
        p1 = right_rotate(a, 2)
        p2 = right_rotate(a, 13)
        p3 = right_rotate(a, 22)
        s0 = "{:032b}".format(int(p1, 2) ^ int(p2, 2) ^ int(p3, 2))

        # maj
        p1 = int(a, 2) & int(b, 2)
        p2 = int(a, 2) & int(c, 2)
        p3 = int(b, 2) & int(c, 2)
        maj = "{:032b}".format(p1 ^ p2 ^ p3)

        # temp2
        temp2 = int((int(s0, 2) + int(maj, 2)) % math.pow(2, 32))
        temp2 = "{:032b}".format(temp2)

        h = g
        g = f
        f = e

        e_int = int((int(d, 2) + int(temp1, 2)) % math.pow(2, 32))
        e = "{:032b}".format(e_int)

        d = c
        c = b
        b = a

        a_int = int((int(temp1, 2) + int(temp2, 2)) % math.pow(2, 32))
        a = "{:032b}".format(a_int)

    # Step 7 : Modify Final Values
    h0_int = int((h0 + int(a, 2)) % math.pow(2, 32))
    h0 = "{:032b}".format(h0_int)

    h1_int = int((h1 + int(b, 2)) % math.pow(2, 32))
    h1 = "{:032b}".format(h1_int)

    h2_int = int((h2 + int(c, 2)) % math.pow(2, 32))
    h2 = "{:032b}".format(h2_int)

    h3_int = int((h3+ int(d, 2)) % math.pow(2, 32))
    h3 = "{:032b}".format(h3_int)

    h4_int = int((h4 + int(e, 2)) % math.pow(2, 32))
    h4 = "{:032b}".format(h4_int)

    h5_int = int((h5 + int(f, 2)) % math.pow(2, 32))
    h5 = "{:032b}".format(h5_int)

    h6_int = int((h6 + int(g, 2)) % math.pow(2, 32))
    h6 = "{:032b}".format(h6_int)

    h7_int = int((h7 + int(h, 2)) % math.pow(2, 32))
    h7 = "{:032b}".format(h7_int)

    # Step 8 : Concatenate Final Hash
    digest = ""

    h0_hex = "{:08x}".format(int(h0,2))
    digest += h0_hex

    h1_hex = "{:08x}".format(int(h1,2))
    digest += h1_hex

    h2_hex = "{:08x}".format(int(h2,2))
    digest += h2_hex

    h3_hex = "{:08x}".format(int(h3,2))
    digest += h3_hex

    h4_hex = "{:08x}".format(int(h4,2))
    digest += h4_hex

    h5_hex = "{:08x}".format(int(h5,2))
    digest += h5_hex

    h6_hex = "{:08x}".format(int(h6,2))
    digest += h6_hex

    h7_hex = "{:08x}".format(int(h7,2))
    digest += h7_hex

    # Printing Part

    print("Size by OS : ", original_size)
    print("Digest : ", digest)

    return digest


# Testing Part
filename = "test.txt"
# sha256(filename)