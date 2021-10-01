import os
import io
from PIL import Image, ImageFile
import math
import random
ImageFile.LOAD_TRUNCATED_IMAGES = True

from array import array

def convert_ord_to_bin(ordinal):
  return bin(ordinal)[2:]

def convert_bin_to_byte(s):
  return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def convert_ord_to_byte(ordinal):
  return convert_bin_to_byte(convert_ord_to_bin(ordinal))

def binary_8base(binary):
  if(len(binary)!=8):
    binary_8 = ""
    for j in range(8-len(binary)):
      binary_8 +="0"
    for i in binary:
      binary_8 += str(i)
    return binary_8
  else:
    return binary
  
def change_lsb(bits, b):
  return (bits & ~1) | b
  
  
def readimage(path):
  count = os.stat(path).st_size / 2
  with open(path, "rb") as f:
    return bytearray(f.read())
 
  
def readimage2(path, type = "BMP"):
  img = Image.open(path, mode='r')
  print(img.format)

  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format=type)
  
  return img_byte_arr.getvalue()

def write_image(path, stego):
  byteimg = io.BytesIO(stego)
  image = Image.open(byteimg)
  image.save(path)
  image.save("compressed_"+path,optimize=True,quality=30) 
  
def rms(cover, stego):
  m = len(cover)
  n = len(stego)
  
  total=0
  for i in range(m):
    total+= (cover[i] - stego[i])^2
  
  return math.sqrt(total/(m*n))

def prns(cover, stego):
  return 20 * math.log(255/rms(cover,stego),10)
 
# for i in range(5): 
#   random.seed(3)
#   print(random.randrange(5))
#   print(random.randrange(5))
#   print(random.randrange(5))
#   print(random.randrange(5))
#   print(random.randrange(5))
#   print(random.randrange(5))
#   print()