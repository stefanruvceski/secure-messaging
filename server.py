import socket
import rsa

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

private_key = ''
public_key = ''

def save_client_public_key(key):
    print(key)
    with open('client_public.pem', mode='wb') as publicfile:
        publicfile.write(key)
def load_public_key():
    with open('client_public.pem', mode='rb') as publicfile:
        keydata = publicfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(keydata)

    return pubkey
def create_keys():
    (pubkey, privkey) = rsa.newkeys(3072)
    priv = rsa.PrivateKey._save_pkcs1_pem(privkey)
    pub = rsa.PublicKey._save_pkcs1_pem(pubkey)

    with open('private.pem', mode='wb') as privatefile:
        privatefile.write(priv)

    with open('public.pem', mode='wb') as publicfile:
        publicfile.write(pub)

def load_keys():
    privkey=''
    pubkey = ''
    with open('private.pem', mode='rb') as privatefile:
        keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)

    with open('public.pem', mode='rb') as publicfile:
        keydata = publicfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(keydata)

    return privkey,pubkey

def encrypt_message(message,key):
    print(message)
    encoded = message.encode('utf8')
    return rsa.encrypt(encoded,key)

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            print('Server open on '+HOST + ':'+str(PORT)+' and listening!')
            conn, addr = s.accept()
            data = conn.recv(1024)
            save_client_public_key(data)
            conn.sendall(rsa.PublicKey._save_pkcs1_pem(public_key))
            #posalji public key
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    text = data.decode()
                    if not data:
                        continue 
                    elif text == 'bye':
                        break
                    print('received: ' + text)
                    conn.sendall(input().encode())

if __name__ == '__main__':
    #create_keys()
    private_key, public_key = load_keys()
    connection()