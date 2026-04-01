import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đã sửa đường dẫn import theo cấu trúc folder của bạn
from ui.rsa import Ui_MainWindow 
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Cấu hình Port 3636
        self.base_url = "http://127.0.0.1:3636/api/rsa"
        
        # Kết nối các nút bấm
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = f"{self.base_url}/generate_keys"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Thông báo", data["message"])
            else:
                print("Lỗi server khi tạo key")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối tới Server: {e}")

    def call_api_encrypt(self):
        url = f"{self.base_url}/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # FIX: Đổi .setText thành .setPlainText
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])
                QMessageBox.information(self, "Thành công", "Đã mã hóa dữ liệu!")
            else:
                print("Lỗi khi gọi API Encrypt")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_decrypt(self):
        url = f"{self.base_url}/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # FIX: Đổi .setText thành .setPlainText
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])
                QMessageBox.information(self, "Thành công", "Đã giải mã dữ liệu!")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_sign(self):
        url = f"{self.base_url}/sign"
        payload = {"message": self.ui.txt_info.toPlainText()}
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # FIX: Đổi .setText thành .setPlainText
                self.ui.txt_sign.setPlainText(data["signature"])
                QMessageBox.information(self, "Thành công", "Đã ký tên thành công!")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_verify(self):
        url = f"{self.base_url}/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    QMessageBox.information(self, "Xác thực", "Chữ ký hợp lệ (Verified Successfully)!")
                else:
                    QMessageBox.warning(self, "Xác thực", "Chữ ký SAI hoặc dữ liệu đã bị sửa đổi!")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())