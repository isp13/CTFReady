import random
import base64

def crypt_the_text(text):
    arr = [ord(x) for x in text]
    for i in range(len(text)):
        arr[i] ^= random.randint(0, 255)
        arr[len(text) - i - 1] ^= random.randint(0, 255)
    ciphered = base64.b64encode(bytes(arr))
    return ciphered.decode()

def decrypt_the_text(text):
    bytearr=str.encode(text)#!

    arr=str(base64.b64decode(bytearr))
    
    arr1 = [ord(x) for x in arr]

    rand_arr = []
    for i in range(len(text)*2):
    	rand_arr.append(random.randint(0, 255))
    rand_arr = rand_arr[::-1]

    count=0
    for i in range(len(text)-1, -1, -1):
        arr1[i] ^= rand_arr[count]
        count+=1
        arr1[len(text) - i - 1] ^= rand_arr[count]
        count+=1

    # arr2 = base64.b64encode(bytes(arr1))
    return ''.join([chr(x) for x in arr1])




if __name__ == '__main__':
    random.seed(1337)
    text = open('ciphertext.txt').read() # этого файла нет, вам надо его восстановить
    ciphertext = decrypt_the_text(text)
    with open('origin.txt', 'w') as f:
        f.write(str(ciphertext))
