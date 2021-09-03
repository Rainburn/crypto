from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .crypto_algorithm.playfair import *
from .crypto_algorithm.affine import *
from .crypto_algorithm.vigenere import *


# Encrypt Type Guide :
# 1 - Vigenere
# 2 - Full Vigenere
# 3 - Auto-key Vigenere
# 4 - Extended Vigenere
# 5 - Playfair Cipher
# 6 - Affine Cipher

def home(request):

    return render(request, 'encryptor/home.html', {

    })


def affine_enc_page(request):
    return render(request, 'encryptor/affine.html')

def playfair_enc_page(request):
    return render(request, 'encryptor/playfair.html')

def vigenere_enc_page(request):
    return render(request, 'encryptor/vigenere.html')


def result_playfair_encrypt(request):

    if (request.method == "POST"):

        form = EncryptForm(request.POST)

        if form.is_valid():

            plain = form.cleaned_data['plain']
            key = form.cleaned_data['key']
            result = playfair_encrypt(plain, key)

            return render(request, 'encryptor/result.html', {
                'plain' : plain,
                'key' : key,
                'cipher' : result,
            })

        else :
            return HttpResponse('<h1>Form invalid</h1>')

    else :
        return HttpResponse('<h1>Invalid Access</h1>')


def result_vigenere_encrypt(request):
    if (request.method == "POST"):

        form = EncryptForm(request.POST)

        if form.is_valid():

            plain = form.cleaned_data['plain']
            key = form.cleaned_data['key']
            result = vigenere_encrypt(plain, key)

            return render(request, 'encryptor/result.html', {
                'plain' : plain,
                'key' : key,
                'cipher' : result,
            })

        else :
            return HttpResponse('<h1>Form invalid</h1>')

    else :
        return HttpResponse('<h1>Invalid Access</h1>')


def result_affine_encrypt(request):

    if (request.method == "POST"):

        form = AffineEncryptForm(request.POST)

        if form.is_valid():

            plain = form.cleaned_data['plain']
            m = int(form.cleaned_data['m'])
            b = int(form.cleaned_data['b'])
            result = affine_encrypt(plain, m, b)

            return render(request, 'encryptor/result_affine.html', {
                'plain' : plain,
                'm' : m,
                'b' : b,
                'cipher' : result,
            })

        else :
            return HttpResponse('<h1>Form invalid</h1>')

    else :
        return HttpResponse('<h1>Invalid Access</h1>')


def result_playfair_decrypt(request):

    if (request.method == "POST"):

        form = DecryptForm(request.POST)

        if form.is_valid():

            cipher = form.cleaned_data['cipher']
            key = form.cleaned_data['key']
            result = playfair_decrypt(cipher, key)

            return render(request, 'encryptor/result.html', {
                'cipher' : cipher,
                'key' : key,
                'plain' : result,
            })

        else :
            return HttpResponse('<h1>Form invalid</h1>')

    else :
        return HttpResponse('<h1>Invalid Access</h1>')


def result_vigenere_decrypt(request):
    if (request.method == "POST"):

        form = DecryptForm(request.POST)

        if form.is_valid():

            cipher = form.cleaned_data['cipher']
            key = form.cleaned_data['key']
            result = vigenere_decrypt(cipher, key)

            return render(request, 'encryptor/result.html', {
                'cipher' : cipher,
                'key' : key,
                'plain' : result,
            })

        else :
            return HttpResponse('<h1>Form invalid</h1>')

    else :
        return HttpResponse('<h1>Invalid Access</h1>')

def result_affine_decrypt(request):

    if (request.method == "POST"):

        form = AffineDecryptForm(request.POST)

        if form.is_valid():

            cipher = form.cleaned_data['cipher']
            m = int(form.cleaned_data['m'])
            b = int(form.cleaned_data['b'])
            result = affine_decrypt(cipher, m, b)

            return render(request, 'encryptor/result_affine.html', {
                'cipher' : cipher,
                'm' : m,
                'b' : b,
                'plain' : result,
            })

        else :
            return HttpResponse('<h1>Form invalid</h1>')

    else :
        return HttpResponse('<h1>Invalid Access</h1>')