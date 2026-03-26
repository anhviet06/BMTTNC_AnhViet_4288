from flask import Flask, render_template, request
from cipher.playfair.playfair_cipher import PlayFairCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/playfair")
def playfair_page():
    return render_template('playfair.html')

@app.route("/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form.get('inputPlainText')
    key = request.form.get('inputKeyPlain')
    
    cipher = PlayFairCipher()
    # Logic theo đúng file playfair_cipher.py của bạn
    matrix = cipher.tao_ma_tran_playfair(key)
    result = cipher.ma_hoa_playfair(text, matrix)
    
    # TRẢ VỀ TRANG CŨ KÈM KẾT QUẢ
    return render_template('playfair.html', 
                           result_encrypt=result, 
                           old_text_encrypt=text, 
                           old_key_encrypt=key)

@app.route("/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form.get('inputCipherText')
    key = request.form.get('inputKeyCipher')
    
    cipher = PlayFairCipher()
    matrix = cipher.tao_ma_tran_playfair(key)
    result = cipher.giai_ma_playfair(text, matrix)
    
    # TRẢ VỀ TRANG CŨ KÈM KẾT QUẢ
    return render_template('playfair.html', 
                           result_decrypt=result, 
                           old_text_decrypt=text, 
                           old_key_decrypt=key)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3636, debug=True)