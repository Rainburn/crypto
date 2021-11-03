import math

class Elyptic:
  def __init__(self, a, b, p):
    self.a = a
    self.b = b
    self.p = p
    
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
def addition(P, Q, p, a):
  # If point are the same
  if(P.x == Q.x and P.y == Q.y):
    if P.y == 0 :
      return Point(0,0)
    
    m = (3* P.x ** 2 + a) * mod_inv(2 * P.y, p) % p
    x = (m**2 - 2*P.x) % p
    y = (m * (P.x - x) - P.y ) % p

    R = Point(x,y)
    
    return R
    
  # If point not the same
  if(P.x < Q.x):
    m = (Q.y - P.y) *  mod_inv(Q.x - P.x, p) % p
  elif(P.x > Q.x):
    m = (P.y - Q.y) *  mod_inv(P.x - Q.x, p) % p
  else:
    return Point(0,0)

  x = (m ** 2 - P.x - Q.x ) % p
  y = (m * (P.x - x) - P.y ) % p
  R = Point(x,y)
  
  return R
  
def duplicate(P, p, a):
  if P.y == 0 :
    return Point(0,0)
    
  m = ((3* (P.x**2) + a) * mod_inv(2 * P.y, p)) % p
  x = (m**2 - 2*P.x) % p
  y = (m * (P.x - x) - P.y ) % p

  R = Point(x,y)
  
  return R
  
def multiple(k, P, p, a):
  add = P
  
  for i in range(k-1):
    add = addition(add, P, p, a)
  
  return add
  
def substract(P, Q, p, a):
  Q = Point(Q.x, -1 * Q.y % p)
  
  return addition(P, Q, p, a)
  
def mod_inv(a, m):
  m0 = m
  y = 0
  x = 1
  
  if(m == 1):
    return 0
  
  while (a>1):
    q = a//m
    t = m
    m = a%m
    a = t
    t = y
    
    y = x - q * y
    x = t
    
  if(x<0):
    x = x + m0
  
  return x
  
# P = Point(2,4)
# Q = Point(5,9)

# R = addition(P, Q, 11, 1)
# print(R.x)
# print(R.y)

# R = addition(P, P, 11, 1)
# print(R.x)
# print(R.y)

# P = Point(0,1)
# R = duplicate(P, 5, 1)
# print(R.x)
# print(R.y)
  
# teks = "abc"
# asci = convert_to_ascii(teks)
# print(asci)

class ECC:
  def __init__(self, a, b, p):
    self.a = a
    self.b = b
    self.p = p
    
  def generate_public_keys(self, m, P):
    return multiple(m, P, self.p, self.a)
    
  def generate_private_keys(self, m, pK):
    return multiple(m, pK, self.p, self.a)
  
  def get_points(self):
    P = Point(0,0)
    
    for x in range(self.p * self.p):
      y = pow((x ** 3 + self.a * x + self.b) % self.p, 0.5)
      
      if(y==math.floor(y) and y!=0):
        new_point = Point(x, int(y))
        P = new_point
        break;
    
    if(P.x == 0 and P.y == 0):
      return 'No Points Found!'
    
    points = [P]
    count = 1
  
    for i in range(2, self.p ** 2):
      point = multiple(i, P, self.p, self.a)
      
      if(point.x == 0 and point.y == 0):
        break;
      
      if(point.y != 0):
        points.append(point)
        count+=1
      
    data = {}
    data['points'] = sorted(points, key = lambda x: (x.x, x.y))
    data['count'] = count
    return data
  
  def encoded(self, points = []):
    if (not len(points)):
      points = self.get_points()['points']

    encoded = {}
    for i in range(len(points)):
      encoded[(points[i].x, points[i].y)] = chr(i % 128)
    
    # print("halo ink")
    # print(encoded)
    return encoded
  
  def encrypt(self, plaintext, k, P, pb):
    encoded = self.encoded()
    
    enc = {
      'text': '',
      'encoding': []
    }

    for c in plaintext:
      kB = self.generate_public_keys(k,P)
      kP = self.generate_private_keys(k, pb)
      
      # kB = multiple(k, P, self.p, self.a)
      # kP = multiple(k, pb, self.p, self.a)
      
      Pm = (0,0)
      for point, encoded_char in encoded.items():
        if encoded_char == c:
          Pm = point
      
      Pc = (kB, addition(Point(Pm[0],Pm[1]), kP, self.p, self.a))
      Pc = ((Pc[0].x, Pc[0].y), (Pc[1].x, Pc[1].y))
      enc['encoding'].append(Pc)
      enc['text'] += encoded[Pc[1]]
    
    enc['text'] = list(map(ord, enc['text']))
    return enc
              
  def decrypt(self, ciphertext, b):
    # cipher = ciphertext.split(' ')
    # cipher_encoded = []
    # for c in cipher:
    #   a = list(map(int, cip.split(',')))
    #   cipher_encoded.append(((a[0],a[1]), (a[2], a[3])))
    
    decoded = self.encoded()
    
    plaintext = ''
    
    for c in ciphertext:
      bKb = multiple(b, Point(c[0][0], c[0][1]), self.p, self.a)
      d = substract(Point(c[1][0], c[1][1]), bKb, self.p, self.a)
      plaintext += decoded[(d.x,d.y)]
      
    return plaintext
    
a = ECC(-1, 188, 751)
points = a.get_points()
list_points = list(points.values())
print(list_points[0][0].x, list_points[0][0].y)
public = a.generate_public_keys(-1, Point(0,375))
private = a.generate_private_keys(188, Point(0,375))

print(public.x, public.y)
print()
print(private.x, public.y)
enc = a.encrypt("inka", 2, Point(0,375), Point(0,375))
print("enc", enc)

dec = a.decrypt(enc["encoding"], 188)
print("dec", dec)
