print("MAIN WINDOW LOADED")
import tkinter as tk
import os
from ui.login_window import LoginWindow

def main():
    # 1. Kiểm tra và đảm bảo thư mục dữ liệu tồn tại
    # Điều này tránh lỗi khi file chạy lần đầu và không tìm thấy file .txt
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # 2. Khởi tạo cửa sổ gốc (root)
    root = tk.Tk()
    root.title("Phone Book Management System")
    
    # 3. Khởi tạo cửa sổ đăng nhập
    # Truyền 'root' vào để LoginWindow quản lý vòng đời cửa sổ
    LoginWindow(root)
    
    # 4. Bắt đầu vòng lặp sự kiện
    root.mainloop()

if __name__ == "__main__":
    main()