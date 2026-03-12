from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher 
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher
app = Flask(__name__)


#cipher
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})


#vigenere
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})


#Playfair cipher
playfair_cipher = PlayFairCipher()

# 1. API Tạo ma trận
@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_tao_ma_tran():
    data = request.json
    khoa = data['key']
    ma_tran_playfair = playfair_cipher.tao_ma_tran_playfair(khoa)
    return jsonify({'playfair_matrix': ma_tran_playfair})

# 2. API Mã hóa
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_ma_hoa():
    data = request.json
    van_ban_nguon = data['plain_text']
    khoa = data['key']
    
    # Tạo ma trận từ khóa trước khi mã hóa
    ma_tran = playfair_cipher.tao_ma_tran_playfair(khoa)
    van_ban_ma_hoa = playfair_cipher.ma_hoa_playfair(van_ban_nguon, ma_tran)
    
    return jsonify({'encrypted_text': van_ban_ma_hoa})

# 3. API Giải mã
@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_giai_ma():
    data = request.json
    van_ban_ma_hoa = data['cipher_text']
    khoa = data['key']
    # Tạo ma trận từ khóa trước khi giải mã
    ma_tran = playfair_cipher.tao_ma_tran_playfair(khoa)
    van_ban_da_giai_ma = playfair_cipher.giai_ma_playfair(van_ban_ma_hoa, ma_tran)
    return jsonify({'decrypted_text': van_ban_da_giai_ma})
#Rail Fence
railfence_cipher = RailFenceCipher()
#API Mã hóa
@app.route('/api/railfence/encrypt', methods=['POST'])
def ma_hoa():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = railfence_cipher.ma_hoa_duong_ray(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})
#API Giải mã
@app.route('/api/railfence/decrypt', methods=['POST'])
def giai_ma():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])

    decrypted_text = railfence_cipher.giai_ma_duong_ray(cipher_text, key)
    
    return jsonify({'decrypted_text': decrypted_text})
    
# TRANSPOSITION CIPHER
transposition_cipher = TranspositionCipher()
#API Mã hóa
@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    encrypted_text = transposition_cipher.ma_hoa(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})
#API Giải Mã
@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    decrypted_text = transposition_cipher.giai_ma(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)