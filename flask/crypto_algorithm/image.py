from utils_3 import *
import time
def embed_image_sequential(input_file, output_file, type="BMP"):
  # Read image Images
  b_array_list = readimage2(input_file, type)   

  message = "Hi humans! Thank you for listening to Inka's TEDx. Have a good year"
  message_byte = bytearray(message, "utf-8")

  message_bin = []

  # Change from byte array to binary array
  for byte in message_byte:
    message_bin.append(convert_ord_to_bin(byte))

  # Change from binary array to 8-base binary array
  message_bin_8 = []
  for byte in message_bin:

    if(len(byte)!=8):
        for j in range(8-len(byte)):
          message_bin_8.append(0)
          
    for i in byte:
      message_bin_8.append(i)
  for i in message_bin_8:
    print(i, end="")
    
  # TODO: count if the message are fit enough in the image
  
  # Insert secret message into cover object
  b_array_list_stego = bytearray() # The stego object
  print("message")
  print(len(message_bin_8))
  for i in range(0,len(b_array_list), 1):
    if(i >= 1000 and i<=1000+len(message_bin_8)-1):
      ordinal = b_array_list[i]
      binary = binary_8base(convert_ord_to_bin(ordinal))
      bin_message = int(message_bin_8[i%1000])
      binary_changed = change_lsb(int(binary),bin_message)
      byte_changed = convert_bin_to_byte(str(binary_changed))
      b_array_list_stego+=byte_changed
    else:
      b_array_list_stego+=convert_ord_to_byte(b_array_list[i])
  #     b_array_list_stego+=convert_ord_to_byte(b_array_list[i+1])
  #     b_array_list_stego+=convert_ord_to_byte(b_array_list[i+2])
  
  # for i in range(len(b_array_list)%3):
  #   b_array_list_stego+=convert_ord_to_byte(b_array_list[i])

  print()
  print(len(b_array_list))
  print(len(b_array_list_stego))
  print("PRNS")
  print(b_array_list==b_array_list)
  print(rms(b_array_list,b_array_list))
  print(rms(b_array_list,b_array_list_stego))
  print(b_array_list==b_array_list_stego)
  print()
  print()

  # Save stego image
  write_image(output_file, b_array_list_stego)

def extract_image_sequential(input_file):
  # Read image Images
  b_array_list2 = readimage2(input_file)  
  message = ""
  for i in range(1000,1536):
    ordinal = b_array_list2[i]
    binary = convert_ord_to_bin(ordinal)
    # print(binary)
    bin_message = int(binary) & 1
    message += str(bin_message)
  print(message)
  message_byte = convert_bin_to_byte(message)
  print(message_byte)



def embed_image_random(input_file,output_file,seed):
  random.seed(seed)
  
  # Read image Images
  b_array_list = readimage2(input_file)   

  message = "Hi humans! Thank you for listening to Inka's TEDx. Have a good year"
  message_byte = bytearray(message, "utf-8")

  message_bin = []

  # Change from byte array to binary array
  for byte in message_byte:
    message_bin.append(convert_ord_to_bin(byte))

  # Change from binary array to 8-base binary array
  message_bin_8 = []
  for byte in message_bin:

    if(len(byte)!=8):
        for j in range(8-len(byte)):
          message_bin_8.append(0)
          
    for i in byte:
      message_bin_8.append(i)
  for i in message_bin_8:
    print(i, end="")
  
  # Insert secret message into cover object
  b_array_list_stego = bytearray() # The stego object
  print("message")
  print(len(message_bin_8))
  
  i=0 # Initial check
  j=1000 # Starting point of message
  k=0 # length of message
  while(i<len(b_array_list)):
    if(i==j and k<len(message_bin_8)):
      
      ordinal = b_array_list[i]
      binary = binary_8base(convert_ord_to_bin(ordinal))
      bin_message = int(message_bin_8[i%j])
      binary_changed = change_lsb(int(binary),bin_message)
      byte_changed = convert_bin_to_byte(str(binary_changed))
      b_array_list_stego+=byte_changed
      
      key = random.randrange(2,5)
      print(i)
      j+=key
      k+=1
    else:
      b_array_list_stego+=convert_ord_to_byte(b_array_list[i])
    i += 1
    
  print("k")
  print(k)

  print(len(b_array_list))
  print(len(b_array_list_stego))
  print(b_array_list==b_array_list_stego)

  # Save stego image
  write_image(output_file, b_array_list_stego)

def extract_image_random(input_file, seed):
  random.seed(seed)
  
  # Read image Images
  b_array_list2 = readimage2(input_file)  
  message = ""
  length = 536 # TODO: NEED TO FIGURE THIS OUT
  
  i=1000 # Starting point of message
  k=0 # Length of message
  
  while(k<length):
    ordinal = b_array_list2[i]
    binary = convert_ord_to_bin(ordinal)
    bin_message = int(binary) & 1
    message += str(bin_message)
    print(i)
    key = random.randrange(2,5)
    i+=key
    k+=1

  print(message)
  message_byte = convert_bin_to_byte(message)
  print(message_byte)
  
# MAIN PROGRAM
embed_image_sequential("png_sample.png", "png_secret_sample.png", "PNG")
# embed_image_random("sample.bmp", "secret_sample_random.bmp", 2)
# extract_image_sequential("secret_sample1.bmp")
# extract_image_random("secret_sample_random.bmp", 2)