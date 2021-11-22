import os
from rsa import *
from sha256 import *
from digital_signature import *

def set_digital_signature(filename, d, n):
    # read input file
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    # file bit size
    original_size = os.stat(filename).st_size
    
    # hash result
    hash_res = sha256(lines, original_size)
    print(f"SHA256 : {hash_res}")

    # encrypted hash with RSA
    encrypted_hash = rsa_encrypt(hash_res, d, n)
    print(f"encrypted hash: {encrypted_hash}")

    # create new file with format: "key_" + filename and write encrypted hash
    ds_file_name = "ds_" + os.path.splitext(filename)[0] + ".txt"
    f = open(ds_file_name, "w+" )
    ds = f"<ds>{encrypted_hash}</ds>"
    f.write(ds)
    print(ds_file_name + " created!")
    f.close()

    return

def verify_digital_signature_file(filename, e, n):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    if(not file_has_ds(lines)):
        # file bit size
        original_size = os.stat(filename).st_size

        # hash result
        hash_res = sha256(lines, original_size)
        print(f"SHA256 : {hash_res}")

        # read digital signature file
        ds_file = open("ds_"+filename, "r")
        ds_lines = ds_file.readlines()
        ds_file.close()

        for ds in ds_lines:
            continue

        encrypted_hash = ds[4:len(ds)-5]
        decrypted_hash = rsa_decrypt(encrypted_hash, e, n)

        is_same = False
        if (hash_res == decrypted_hash):
            is_same = True
        
        print(f"IS FILE ORIGINAL : {is_same}")
        return is_same
    else:
        verify_digital_signature(filename, e, n)

def file_has_ds(lines): # check if file include digital signature at the bottom
    for line in lines:
        lastline = line
    
    return (lastline[0:4] == "<ds>") and (lastline[len(lastline)-5:len(lastline)] == "</ds>")

filename = "plain_test.txt"

p = 1103
q = 2203
e = 10711
keys = create_keys_rsa(p,q,e)

d = keys['private'][0]
n = keys['private'][1]

set_digital_signature(filename, d, n)
verify_digital_signature_file(filename, e, n)