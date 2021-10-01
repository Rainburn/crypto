from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import wave
import math
import io
import random
from rc4 import *

def read_audio(filename):
    samplerate, data = wavfile.read(filename)
    return samplerate, data


def read_audio_binary(filename):
    with open(filename, "rb") as wavfile:
        input_wav = wavfile.read()
    
    print(len(input_wav))

    rate, data = wavfile.read(io.BytesIO(input_wav))

    reversed_data = data[::-1]

    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    wavfile.write(byte_io, rate, reversed_data)

    output_wav = byte_io.read()

    return output_wav


def write_audio(filename, rate, data):
    dataint16 = np.asarray(data, dtype=np.int16)
    print("Data : ", dataint16)
    wavfile.write(filename, rate, dataint16)


def modify_audio(data):

    data_length = len(data)

    for i in range(data_length):
        data[i][0] = data[i][0] + 1
        data[i][1] = data[i][1] - 1

    return data

def read_file_binary(filename):
    f = open(filename, "rb")

    read_bytes_string = ""

    byte = f.read(1)
    size = 0
    while (byte):
        read_bytes_string = read_bytes_string + chr(ord(byte))

        byte = f.read(1)
        size = size + 1

    print(f"Size : {size}")
    print(f"Read bytes length : {len(read_bytes_string)}")

    f.close()

    return read_bytes_string



def save_file_binary(filename, content):

    content_as_bytearray = []
    for byte in content:
        content_as_bytearray.append(ord(byte)) 

    print(f"Content as byte length : {len(content_as_bytearray)}")

    content_as_bytearray = bytearray(content_as_bytearray)

    f = open(filename, "wb")
    f.write(content_as_bytearray)

    f.close()


def read_audio_wave(filename):
        print("Reading audio....")
        wave_read = wave.open(filename, 'rb')

        # CHUNK_SIZE = 32763  # In bytes.

        CHUNK_SIZE = 32000

        sampleWidth = wave_read.getsampwidth()
        nChannels = wave_read.getnchannels()
        frameRate = wave_read.getframerate()
        frameSize = sampleWidth * nChannels

        chunkFrameCount = CHUNK_SIZE / frameSize # 1 Chunk berisi berapa frame 
        chunkTime = chunkFrameCount / frameRate # Time elapsed in one chunk. In seconds.

        # Get the number of chunks needed to create 3 seconds audio bytes.
        chunkCountByDuration = 0
        while chunkCountByDuration * chunkTime < 34:
            chunkCountByDuration += 1

        # Get the number of chunks needed to hear the audio fully
        chunk_count = math.ceil(wave_read.getnframes() / chunkFrameCount)    

        audioChunks = []

        # Move Audio to Chunk
        for _ in range(chunk_count):
            audioChunk = bytearray()
            for _ in range(int(chunkFrameCount)):
                audioChunk += wave_read.readframes(1)
                audioChunks.append(audioChunk) 

        return audioChunks


def plot_audio_data(data, rate):
    length = data.shape[0] / rate

    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:, 0], label="Left Channel")
    plt.plot(time, data[:, 1], label="Right Channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

def find_max_min_amp(data):
    left_max_amp = 0
    left_min_amp = 0

    right_max_amp = 0
    right_min_amp = 0

    for i in range(len(data)):
        curr_amps = data[i]

        if (curr_amps[0] > left_max_amp):
            left_max_amp = curr_amps[0]
        if (curr_amps[0] < left_min_amp):
            left_min_amp = curr_amps[0]

        if (curr_amps[1] > right_max_amp):
            right_max_amp = curr_amps[1]
        if (curr_amps[1] < right_min_amp):
            right_min_amp = curr_amps[1]
    
    print(f"Left Max Amp : {left_max_amp}")
    print(f"Left Min Amp : {left_min_amp}")
    print(f"Right Max Amp : {right_max_amp}")
    print(f"Right Min Amp : {right_min_amp}")


def convert_data_to_ord(data):
    ord_data = []
    for i in range(len(data)):
        ord_data.append(ord(data[i]))
    
    return ord_data


def convert_ord_to_bytes_string(ord_array):
    ord_str = ""
    for i in range(len(ord_array)):
        ord_str = ord_str + chr(ord_array[i])

    return ord_str


def embed_message(audio_name, embedded_filename, target_filename, key=""):

    rate, audio_data = read_audio(audio_name)
    embedded_data = read_file_binary(embedded_filename)
    length_embedded_data = 0


    if (key != ""): # Use RC4
        embedded_data = rc4_encrypt(embedded_data, key)
        length_embedded_data = len(embedded_data)

    else :
        # Embedded data must be in array of ord, thus we convert

        embedded_data = convert_data_to_ord(embedded_data)
        length_embedded_data = len(embedded_data)


    stego_data = audio_data.copy()
    aud_length = len(audio_data)
    
    # Reduce Available bytes with Metadata

    # Random metadata
    stego_data[0][0] = 0 # Seed
    # random.seed(seed)

    # Embedded Message length metadata
    stego_data[1][0] = length_embedded_data

    # File type
    filetype = embedded_filename.split('.')[1]
    length_filetype = len(filetype)
    
    stego_data[2][0] = length_filetype

    for i in range(length_filetype):
        stego_data[3+i][0] = ord(filetype[i])

    shifts = length_filetype + 3
    avail_space = aud_length - shifts

    # Check if space is enough for embedded data
    if (avail_space < 8 * len(embedded_data)):
        print("Not Enough Space !")
        return 
    

    # Insert all data into cover
    for i in range(len(embedded_data)):
        curr_ord = embedded_data[i]
        ord_in_bin = format(curr_ord, '08b')

        for j in range(len(ord_in_bin)):
            idx = ((i * 8 + j)) % avail_space
            base_2_amp = format(stego_data[shifts+idx][0], 'b')
            
            # Swap LSB
            temp = base_2_amp[0:len(base_2_amp)-1]
            temp = temp + ord_in_bin[j]

            stego_data[shifts+idx][0] = int(temp, 2)


    write_audio(target_filename, rate, stego_data)


    return stego_data



def retrieve_embedded(stego_filename, hidden_filename, key=""):

    rate, stego_data = read_audio(stego_filename)
    aud_length = len(stego_data)

    # Read metadata
    seed = stego_data[0][0]
    random.seed(seed)
    length_hidden_in_byte = stego_data[1][0]
    length_hidden_in_bit = 8 * length_hidden_in_byte

    # Filetype
    length_filetype = stego_data[2][0]
    filetype_as_string = ""

    for i in range(length_filetype):
        filetype_as_string = filetype_as_string + chr(stego_data[3+i][0])

    # Shifts
    shifts = 3 + length_filetype
    avail_space = aud_length - shifts

    hidden_data_as_byte = ""

    count = 0
    fragment = ""
    for i in range(length_hidden_in_bit):
        count = count + 1

        idx = (i) % avail_space
        stego_amp_as_bit = format(stego_data[shifts+idx][0], 'b')

        fragment = fragment + stego_amp_as_bit[len(stego_amp_as_bit)-1]

        if (count == 8):
            fragment_as_dec = int(fragment, 2)
            chr_of_fragment = chr(fragment_as_dec)
            hidden_data_as_byte = hidden_data_as_byte + chr_of_fragment

            fragment = ""
            count = 0

    if (key != ""): # Use RC4
        hidden_data_as_byte = convert_ord_to_bytes_string(rc4_decrypt(hidden_data_as_byte, key))

    save_file_binary(hidden_filename + "." + filetype_as_string, hidden_data_as_byte)

    return 



# Main Here

# Read File
rate, data = read_audio('wavexample.wav')
my_message = "Hello from the another side"

# print(f"Rate : {rate}")
# print(f"Length of DataArray : {len(data)}")

embed_message("wavexample.wav", "count_db.png", "stego_audio_img.wav", "INKABESOKTEDX")

retrieve_embedded("stego_audio_img.wav", "hidden_pic2", "INKABESOKTEDX")