# -*- coding: utf-8 -*-
"""
main.py
--------
DIEM KHOI CHAY chuong trinh demo cho module Contact Management
(Add / Edit / Delete / View / Favorite / Emergency) - phan viec cua Khang
trong do an "Phone Book Management System" (Nhom 8).

CACH CHAY:
    1) (Mot lan duy nhat) Cai thu vien Pillow de xu ly anh dai dien:
           pip install pillow
    2) Chay:
           python main.py

GHI CHU VE TICH HOP VOI NHOM:
Trong he thong hoan chinh, "user dang dang nhap" (current_user_id) se do
module Dang nhap/Dang ky (Account Management - FR-1, do thanh vien khac
trong nhom phu trach) cung cap SAU KHI xac thuc thanh cong (UC2 - Login).
Vi module nay can chay va kiem thu DOC LAP, ta mo phong san mot phien dang
nhap voi user_id = 1 (xem DEMO_USER_ID ben duoi).

Khi ghep noi voi module Login that cua nhom, chi can thay DEMO_USER_ID ben
duoi bang user_id lay tu session dang nhap thuc te, vi du:
    manager = ContactManager(user_id=session.current_user.user_id)
"""

from contact_manager import ContactManager
from gui import PhoneBookApp

DEMO_USER_ID = 1  # <-- Trong he thong that: lay tu module Login (nhom khac)


def main() -> None:
    manager = ContactManager(user_id=DEMO_USER_ID)
    app = PhoneBookApp(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
