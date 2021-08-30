from vigenere import *
from affine import *
from playfair import *

plain = "kripto"

cipher = affine_encrypt(plain, 7, 10)
plain_res = affine_decrypt(cipher, 7, 10)


playfair_encrypt()