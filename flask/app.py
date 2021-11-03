from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from crypto_algorithm.affine import *
from crypto_algorithm.playfair import *
from crypto_algorithm.vigenere import *
from crypto_algorithm.rc4 import *
# from crypto_algorithm.rsa import *
# from crypto_algorithm.paillier import *
from crypto_algorithm.elgamal import *

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def student():
   return render_template('index.html')
                
@app.route('/generate-keys',methods = ['POST', 'GET'])
def generate_keys():
    payload = request.json
    form = payload['data']
    if(form["algo_id"] == "10"): # Elgamal
        g = int(form["g"])
        p = int(form["p"])
        x = int(form["x"])
        k = int(form["k"])
        
        elgamal = Elgamal(p, g, x, k)
        public_key = elgamal.generate_public_keys()
        private_key = elgamal.generate_private_keys()
        return {'public_key': public_key, 'private_key': private_key}
    
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

            elif (algo_id == "7"): # RC4
                key = form['key']
                result = rc4_encrypt(plain, key)
                return {'plain' : plain, 'key' : key, 'cipher' : result}

            elif (algo_id == "8"): # RSA
                e = form['e']
                n = form['n']
                result = rsa_encrypt(plain, e, n)
                return {'plain' : plain, 'e' : e, 'n' : n, 'cipher' : result}

            elif (algo_id == "9"): # Paillier
                g = form['g']
                n = form['n']
                result = paillier_encrypt(plain, g, n)
                return {'plain' : plain, 'g' : g, 'n' : n, 'cipher' : result}
                
            elif (algo_id == "10") : # Elgamal
                g = int(form["g"])
                p = int(form["p"])
                x = int(form["x"])
                k = int(form["k"])
                plaintext = form["text"]
                
                elgamal = Elgamal(p, g, x, k)
                keys = elgamal.generate_public_keys()
                result = elgamal.encrypt(plaintext, keys)
                return {'result': result}
        
        
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
            
            elif (algo_id == "6"): # Affine
                m = form['m']
                b = form['b']
                result = affine_decrypt(cipher, m, b)
                return {'plain' : result, 'm' : m, 'b' : b, 'cipher' : cipher}

            elif (algo_id == "7"): # RC4
                key = form['key']
                result = rc4_decrypt(cipher, key)
                return {'plain' : result, 'key' : key, 'cipher' : cipher}

            elif (algo_id == "8"): # RSA
                d = form['d']
                n = form['n']
                result = rsa_decrypt(cipher, d, n)
                return {'plain' : result, 'd' : d, 'n' : n, 'cipher' : cipher}

            elif (algo_id == "9"): # Paillier
                n = form['n']
                lambd = form['lambda']
                u = form['u']
                result = paillier_decrypt(cipher, n, lambd, u)
                return {'plain' : result, 'n' : n, 'lambda' : lambd, 'u' : u, 'cipher' : cipher}
            
            elif (algo_id == "10") : # Elgamal
                g = int(form["g"])
                p = int(form["p"])
                x = int(form["x"])
                k = int(form["k"])
                plaintext = form["text"]
                
                elgamal = Elgamal(p, g, x, k)
                keys = elgamal.generate_private_keys()
                result = elgamal.decrypt(plaintext, keys)
                return {'result': result}

        
    else :
        return 'Invalid Access'
    
        

if __name__ == '__main__':
   app.run(debug = True)