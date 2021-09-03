
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('affine', affine_enc_page, name="affine_encrypt"),
    path('playfair', playfair_enc_page, name="playfair_encrypt"),
    path('vigenere', vigenere_enc_page, name="vigenere_encrypt"),
    path('result/vigenere/encrypt', result_vigenere_encrypt, name="result"),
    path('result/affine/encrypt', result_affine_encrypt, name="result"),
    path('result/playfair/encrypt', result_playfair_encrypt, name="result"),
    path('result/vigenere/decrypt', result_vigenere_decrypt, name="result"),
    path('result/playfair/decrypt', result_playfair_decrypt, name="result"),
    path('result_affine/decrypt', result_affine_decrypt, name="result")
]
