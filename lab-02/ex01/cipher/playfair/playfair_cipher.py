class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def tao_ma_tran_playfair(self, key):
        # Chuyển J thành I và viết hoa
        key = key.upper().replace("J", "I")
        
        # Tạo danh sách các ký tự duy nhất từ khóa, giữ nguyên thứ tự
        matrix = []
        for char in key:
            if char not in matrix and char.isalpha():
                matrix.append(char)
        
        # Thêm các ký tự còn lại trong bảng chữ cái
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in matrix:
                matrix.append(char)
        
        # Chuyển thành ma trận 5x5
        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def tim_toa_do_ky_tu(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def ma_hoa_playfair(self, plain_text, matrix):
        # Chuẩn hóa văn bản: viết hoa, đổi J thành I, xóa khoảng trắng
        plain_text = plain_text.upper().replace("J", "I").replace(" ", "")
        
        # Xử lý chia cặp (Digraphs) - Quan trọng để giải mã chính xác
        i = 0
        refined_text = ""
        while i < len(plain_text):
            char1 = plain_text[i]
            if i + 1 < len(plain_text):
                char2 = plain_text[i+1]
                if char1 == char2: # Nếu 2 ký tự trùng nhau trong 1 cặp
                    refined_text += char1 + "X"
                    i += 1
                else:
                    refined_text += char1 + char2
                    i += 2
            else: # Nếu lẻ ký tự ở cuối
                refined_text += char1 + "X"
                i += 1
        
        encrypted_text = ""
        for i in range(0, len(refined_text), 2):
            row1, col1 = self.tim_toa_do_ky_tu(matrix, refined_text[i])
            row2, col2 = self.tim_toa_do_ky_tu(matrix, refined_text[i+1])
            
            if row1 == row2: # Cùng hàng
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2: # Cùng cột
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else: # Hình chữ nhật
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        return encrypted_text

    def giai_ma_playfair(self, cipher_text, matrix):
        cipher_text = cipher_text.upper().replace(" ", "")
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            row1, col1 = self.tim_toa_do_ky_tu(matrix, cipher_text[i])
            row2, col2 = self.tim_toa_do_ky_tu(matrix, cipher_text[i+1])
            
            if row1 == row2:
                # Dùng +4 thay vì -1 để tránh lỗi số âm ở một số môi trường
                decrypted_text += matrix[row1][(col1 + 4) % 5] + matrix[row2][(col2 + 4) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 + 4) % 5][col1] + matrix[(row2 + 4) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return decrypted_text