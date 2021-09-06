from flask import Flask, render_template, request
from crypto_algorithm.affine import *
from crypto_algorithm.playfair import *
from crypto_algorithm.vigenere import *

app = Flask(__name__)

@app.route('/')
def student():
   return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():

    if (request.method == "POST"):
        
        form = request.form

        if (form["action"] == "encrypt"):

            plain = form['plain']
            algo_id = form['algorithm']

            if (algo_id == "1"): # Vigenere
                key = form['key']
                result = vigenere_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result}
        
            elif (algo_id == "2"): # Playfair
                key = form['key']
                result = playfair_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result}
            
            elif (algo_id == "3"):
                m = form['m']
                b = form['b']
                result = affine_encrypt(plain, m, b)
                return {'plain' : plain, 'm' : m, 'b' : b, 'cipher' : result}

        else : # action is decrypt
            cipher = form['cipher']
            algo_id = form['algorithm']

            if (algo_id == "1"): # Vigenere
                key = form['key']
                result = vigenere_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
        
            elif (algo_id == "2"): # Playfair
                key = form['key']
                result = playfair_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
            
            elif (algo_id == "3"):
                m = form['m']
                b = form['b']
                result = affine_decrypt(cipher, m, b)
                return {'plain' : result, 'm' : m, 'b' : b, 'cipher' : cipher}

    else :
        return 'Invalid Access'
    
        

if __name__ == '__main__':
   app.run(debug = True)