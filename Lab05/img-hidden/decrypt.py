import sys
from PIL import Image

def decode_image(encoded_image_path):
    # Thêm .convert('RGB') ở đây
    img = Image.open(encoded_image_path).convert('RGB')
    width, height = img.size
    binary_message = ""
    
    for row in range(height):
        for col in range(width):
            # Ép kiểu list để truy cập pixel[color_channel]
            pixel = list(img.getpixel((col, row)))
            
            for color_channel in range(3):
                # Lấy bit cuối cùng của mỗi kênh màu
                binary_message += format(pixel[color_channel], '08b')[-1]
                
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        char = chr(int(byte, 2))
        # Kiểm tra ký tự kết thúc Null
        if char == '\0' or byte == '00000000':
            break
        message += char
        
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
        
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()