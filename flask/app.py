from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from crypto_algorithm.affine import *
from crypto_algorithm.playfair import *
from crypto_algorithm.vigenere import *
from crypto_algorithm.rc4 import *
from crypto_algorithm.rsa import *
from crypto_algorithm.paillier import *
from crypto_algorithm.elgamal import *
from crypto_algorithm.ecc import *
from crypto_algorithm.digital_signature import *

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def student():
   return render_template('index.html')
   
@app.route('/sha',methods = ['POST', 'GET'])
def sha():
    payload = request.json
    form = payload['data']
    
    if(form["method"] == "signing"): # Signing
        d = int(form["d"])
        n = int(form["n"])
        filename = form["filename"]
        output_filename = form["output_filename"]
        
        result = set_digital_signature(filename, d, n, output_filename)
        
        return {'success': result}

    elif (form['method'] == "verifying"): # Verifying
        e = int(form['e'])
        n = int(form['n'])
        filename = form['filename']
        
        result = verify_digital_signature(filename, e, n)
        return {'result' : result}
                
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

    elif (form['algo_id'] == "8"): # RSA
        p = int(form['p'])
        q = int(form['q'])
        e = int(form['e'])

        keys = create_keys_rsa(p, q, e)
        return {'public_key' : keys['public'], 'private_key' : keys['private']}

    elif (form['algo_id'] == "9"): # Paillier
        p = int(form['p'])
        q = int(form['q'])
        g = int(form['g'])
        
        keys = create_keys_paillier(p, q, g)
        return {'public_key' : keys['public'], 'private_key' : keys['private']}
        
    elif (form["algo_id"]=="11"): # ECC
        a = int(form["a"])
        b = int(form["b"])
        p = int(form["p"])
        
        ecc = ECC(a, b, p)
        points = ecc.get_points()
        list_points = list(points.values())
        B = list_points[0][0]
        keys = ecc.generate_public_keys(a, B)
        public_a = ecc.generate_public_keys(a, B)
        public_b = ecc.generate_public_keys(b, B)
        private_a = ecc.generate_private_keys(a, public_b)
        
        return {'public_key' : [public_a.x, public_a.y], 'private_key' : [private_a.x, private_a.y]}
        
        
    
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
                e = int(form['e'])
                n = int(form['n'])
                result = rsa_encrypt(plain, e, n)
                return {'plain' : plain, 'e' : e, 'n' : n, 'cipher' : result}

            elif (algo_id == "9"): # Paillier
                g = int(form['g'])
                p = int(form['p'])
                q = int(form['q'])
                
                n = p * q
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
            
            elif (algo_id == "11") : # ECC
                a = int(form["a"])
                b = int(form["b"])
                p = int(form["p"])
                k = int(form["k"])
                plaintext = form["text"]
                
                ecc = ECC(a, b, p)
                points = ecc.get_points()
                list_points = list(points.values())
                B = list_points[0][0]
                keys = ecc.generate_public_keys(a, B)
                public_a = ecc.generate_public_keys(a, B)
                public_b = ecc.generate_public_keys(b, B)
                private_a = ecc.generate_private_keys(a, public_b)
                
                enc = ecc.encrypt(plaintext, k, B , public_b)
                return {'result': enc["encoding"]}


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
                d = int(form['d'])
                n = int(form['n'])
                result = rsa_decrypt(cipher, d, n)
                return {'plain' : result, 'd' : d, 'n' : n, 'cipher' : cipher}

            elif (algo_id == "9"): # Paillier
                p = int(form['p'])
                q = int(form['q'])
                lambd = int(form['lambda'])
                u = int(form['u'])
                n = p * q
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
            
            elif (algo_id == "11") : # ECC
                a = int(form["a"])
                b = int(form["b"])
                p = int(form["p"])
                plaintext = form["text"]
                
                ecc = ECC(a, b, p)
                points = ecc.get_points()
                list_points = list(points.values())
                
                dec = ecc.decrypt(plaintext, b)
                return {'result': dec}

        
    else :
        return 'Invalid Access'
    
        

if __name__ == '__main__':
   app.run(debug = True)