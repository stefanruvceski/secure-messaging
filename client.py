

import socket
import rsa
from time import  sleep

private_key = ''
public_key = ''

def create_keys():
    (pubkey, privkey) = rsa.newkeys(3072)
    priv = rsa.PrivateKey._save_pkcs1_pem(privkey)
    pub = rsa.PublicKey._save_pkcs1_pem(pubkey)

    with open('private.pem', mode='wb') as privatefile:
        privatefile.write(priv)

    with open('public.pem', mode='wb') as publicfile:
        publicfile.write(pub)

def load_keys():
    with open('private1.pem', mode='rb') as privatefile:
        keydata = privatefile.read()
        priv = rsa.PrivateKey.load_pkcs1(keydata)

    with open('public1.pem', mode='rb') as publicfile:
        keydata = publicfile.read()
        pub = rsa.PublicKey.load_pkcs1(keydata)

    return priv,pub

def save_server_public_key(key):
    print(key)
    with open('server_public.pem', mode='wb') as publicfile:
        publicfile.write(key)

def decrypt_message(message,key):
    decrypted_message = rsa.decrypt(message,key)
    return decrypted_message.decode('utf8')

def connection():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #sleep(2)
        print(rsa.PrivateKey._save_pkcs1_pem(private_key))
        s.sendall(rsa.PublicKey._save_pkcs1_pem(public_key))
        data = s.recv(1024)
        save_server_public_key(data)
        print('Received', data)
        #primi public key
        while True:
            text = input()
            s.sendall(text.encode())
            if(text == 'bye'):
                break;
            data = s.recv(1024)
            print('Received', repr(data.decode()))

if __name__ == '__main__':
    #create_keys()
    private_key,public_key =  load_keys()
    connection()