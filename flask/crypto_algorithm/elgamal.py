from .utils import *

def power(a,b):
  return a**b

class Elgamal:
  def __init__(self,p, g, x, k):
    self.p = p
    self.g = g
    self.x = x
    self.k = k
    
  def generate_public_keys(self):
    y = power(self.g, self.x) % self.p
    return (y, self.g, self.p)
    
  def generate_private_keys(self):
    return (self.x, self.p)
  
  def encrypt(self, plaintext, public_key):    
    ciphertext = []
    
    for m in plaintext:
      if(isinstance(m, str)):
        m = ord(m)
      a = power(public_key[1], self.k) % public_key[2]
      b = power(public_key[0], self.k) * m % public_key[2]
      
      ciphertext.append((a,b))
    
    return ciphertext
  
  def decrypt(self, cipher, private_key):
    
    if(isinstance(cipher,str)):
      cipher_split = cipher.split(' ')
      cipher = []
      
      for pair in cipher_split:
        cipher.append(pair.split(','))
          
    plainteks = ''
    for p in cipher:
      a = p[0]
      b = p[1]
      
      ax = power(int(a), (private_key[1]-private_key[0]-1)) % private_key[1]
      plainteks += chr(int(b) * ax % private_key[1])
      
    return plainteks
  
# p = 2357
# g = 2
# x = 1751
# y = power(g,x) % p
# m = 2035
# k = 1520


# a = Elgamal(2357, 2, 1751, 1520)
# public_key = a.generate_public_keys()
# enc = a.encrypt("tugas kripto", public_key)
# print(public_key)
# print(enc)

# b = Elgamal(2357, 2, 1751, 1520)
# private_key = b.generate_private_keys()
# dec = b.decrypt(enc, private_key)
# print(dec)
# dec = b.decrypt(enc, private_key)
# print(dec)


