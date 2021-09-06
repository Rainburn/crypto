from .vigenere import *
from .affine import *
from .playfair import *


key = "JALAN GANESHA SEPULUH"
plain_playfair = "temui ibu nanti malam"

cipher = playfair_encrypt(plain_playfair, key)
plain_res = playfair_decrypt(cipher, key)

print(cipher)
print(plain_res)