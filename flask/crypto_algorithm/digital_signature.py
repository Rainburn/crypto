import os
from rsa import *
from sha256 import *


def set_digital_signature(filename, e, n):

    f = open(filename, "r")

    lines = f.readlines()

    f.close()

    original_size = os.stat(filename).st_size

    # SHA256 for FILENAME
    hash_res = sha256(lines, original_size)

    print(f"SHA256 : {hash_res}")

    encrypted_hash = rsa_encrypt(hash_res, e, n)

    # decrypted_hash = rsa_decrypt(encrypted_hash, d, n)

    print(f"Encrypted Hash : {encrypted_hash}")
    # print(f"Decrypted Hash : {decrypted_hash}")

    f = open(filename, "a")
    ds = f"<ds>{encrypted_hash}</ds>"

    for i in range(4):
        f.write("\n")
    f.write(ds)
    f.close()

    return


def verify_digital_signature(filename, d, n):

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    for line in lines:
        print(line)

    residual_size = 0
    space_size = 4

    residual_size += space_size

    key_line = lines[len(lines) - 1]
    ds_size = 0

    for c in key_line:
        ds_size += 1

    residual_size += ds_size


    # Separate content and ds here
    total_lines = len(lines)

    ds = lines[total_lines-1]
    total_newline_found = 0
    # Count the FREE \n
    for num_line in range(total_lines-2, (total_lines - 1)-5, -1):
        if (lines[num_line] == "\n"):
            total_newline_found += 1

    original_content = ""

    if (total_newline_found != space_size): # End of real document is NOT \n

        temp = lines[total_lines-5]
        temp = temp[0:(len(temp) - 1)]


        lines[total_lines-5] = temp
        
        original_content = lines[0:total_lines-4]

    
    else : # total_newline_found = space_size, end of real document is \n

        original_content = lines[0:total_lines-5]


    # Verify File Here
    hash_res = sha256(original_content, os.stat(filename).st_size - residual_size)

    # Decrypt Digital Signature
    encrypted_hash = ds[4:len(ds)-5]
    decrypted_hash = rsa_decrypt(encrypted_hash, d, n)

    # print("Total Lines :", len(lines))
    # print(original_content)

    print("Residual size : ", residual_size)
    print("Size reduced by residual : ", os.stat(filename).st_size - residual_size)
    print("Size by OS : ", os.stat(filename).st_size)

    is_same = False
    if (hash_res == decrypted_hash):
        is_same = True

    print(f"IS FILE ORIGINAL : {is_same}")

    return is_same


# Testing part 
filename = "test.txt"

# RSA with p = 1103, q = 2203, e = 10711. Will be used for RSA Encryption
p = 1103
q = 2203
e = 10711
keys = create_keys_rsa(p, q, e)

d = keys['private'][0]
n = keys['private'][1]

# Pake fungsi ini kalo mau sign suatu file
# Remember, signing pake PRIVATE KEY (d). Dengan d yang cukup besar, proses signing agak lama

# set_digital_signature(filename, d, n)

# Pake fungsi ini buat verify signature yang ada pada file
# Verify digital signature pake public key

verify_digital_signature(filename, e, n)

