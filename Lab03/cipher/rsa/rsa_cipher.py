import rsa
import os

if not os.path.exists('cipher/rsa/keys'):
    os.makedirs('cipher/rsa/keys')


class RSACipher:
    def __init__(self):
        pass
#generate_keys
    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        with open('cipher/rsa/keys/publicKey.pem', 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open('cipher/rsa/keys/privateKey.pem', 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))
#load_keys
    def load_keys(self):
        with open('cipher/rsa/keys/publicKey.pem', 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open('cipher/rsa/keys/privateKey.pem', 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return private_key, public_key
#encrypt
    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('ascii'), key)
#decrypt
    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except:
            return False
#sign
    def sign(self, message, key):
        # Đã cập nhật từ 'SHA-1' sang 'SHA-256'
        return rsa.sign(message.encode('ascii'), key, 'SHA-256')
#verify
    def verify(self, message, signature, key):
        try:
            # rsa.verify trả về phương thức hash nếu khớp, nên ta so sánh với 'SHA-256'
            return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-256'
        except:
            return False