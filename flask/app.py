from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from crypto_algorithm.affine import *
from crypto_algorithm.playfair import *
from crypto_algorithm.vigenere import *

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def student():
   return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():

    print('halo')
    if (request.method == "POST"):
        
        # form = request.form
        # print(request)
        # print(form)
        # print("action")
        
        
        payload = request.json
        form = payload['data']

        if (form["action"] == "encrypt"):

            plain = form['text']
            algo_id = form['algorithm']

            if (algo_id == "1"): # Vigenere
                key = form['key']
                result = vigenere_encrypt(plain, key)
                return jsonify({'plain' : plain, 'key' : key, 'cipher' : result})
                
            elif (algo_id == "2"): # Full Vigenere
                key = form['key']
                [result, table] = full_vigenere_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result, 'table' : table}
                
            elif (algo_id == "3"): # Auto-Key Vigenere
                key = form['key']
                result = auto_key_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result}
                
            elif (algo_id == "4"): # Extended Vigenere
                key = form['key']
                result = extended_vigenere_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result}
        
            elif (algo_id == "5"): # Playfair
                key = form['key']
                result = playfair_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result}
            
            elif (algo_id == "6"): # Affine
                m = form['m']
                b = form['b']
                result = affine_encrypt(plain, m, b)
                return {'plain' : plain, 'm' : m, 'b' : b, 'cipher' : result}

        else : # action is decrypt
            cipher = form['text']
            algo_id = form['algorithm']

            if (algo_id == "1"): # Vigenere
                key = form['key']
                result = vigenere_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
                
            elif (algo_id == "2"): # Full Vigenere
                key = form['key']
                table = form['table']
                result = full_vigenere_decrypt(cipher, key, table)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
                
            elif (algo_id == "3"): # Auto-key vigenere
                key = form['key']
                result = auto_key_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
                
            elif (algo_id == "4"): # Extended Vigenere
                key = form['key']
                result = extended_vigenere_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
                
            elif (algo_id == "5"): # Playfair
                key = form['key']
                result = playfair_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}
            
            elif (algo_id == "6"):
                m = form['m']
                b = form['b']
                result = affine_decrypt(cipher, m, b)
                return {'plain' : result, 'm' : m, 'b' : b, 'cipher' : cipher}

    else :
        return 'Invalid Access'
    
        

if __name__ == '__main__':
   app.run(debug = True)