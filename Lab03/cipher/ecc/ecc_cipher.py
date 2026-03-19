import ecdsa, os

# Đảm bảo thư mục lưu khóa tồn tại
if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        # Tạo khóa riêng tư (Signing Key)
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
        vk = sk.get_verifying_key() # Lấy khóa công khai
        
        with open('cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())
            
        with open('cipher/ecc/keys/publicKey.pem', 'wb') as p:
            p.write(vk.to_pem())
        print("Đã tạo và lưu khóa thành công.")

    def load_keys(self):
        with open('cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
        with open('cipher/ecc/keys/publicKey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
        return sk, vk

    def sign(self, message, key):
        # Ký dữ liệu (dùng utf-8 để hỗ trợ tiếng Việt)
        return key.sign(message.encode('utf-8'))

    def verify(self, message, signature, key):
        try:
            # key ở đây nên là vk (verifying key)
            return key.verify(signature, message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            return False