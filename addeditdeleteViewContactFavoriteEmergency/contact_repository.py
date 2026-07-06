# -*- coding: utf-8 -*-
"""
contact_repository.py
----------------------
Tang truy xuat du lieu (Data Access Layer), tuong ung voi kho du lieu
"D2 - Contact Data" trong so do luong du lieu DFD (Muc III bao cao).

Theo NFR-5 (Development Ability): "The system is developed using Python and
uses a text file (text.txt) for data storage." -> Toan bo danh ba duoc luu
trong MOT FILE VAN BAN ten "text.txt", KHONG dung co so du lieu that.

Moi dong trong text.txt la MOT ban ghi Contact duoc ma hoa dang JSON
(ky thuat "JSON Lines"). Van la file van ban thuan (dung yeu cau NFR-5),
nhung doc/ghi an toan voi tieng Viet co dau, dau phay, ky tu dac biet trong
ten/dia chi... ma khong bi loi nhu khi tach chuoi bang dau "," don gian.

ContactRepository CHI lam nhiem vu doc/ghi file - KHONG chua logic nghiep vu
(validate, kiem tra trung so dien thoai...). Logic nghiep vu nam o
ContactManager (contact_manager.py).
"""

from __future__ import annotations
import json
import os
from typing import List

from models import Contact


class ContactRepository:
    """Doc va ghi danh sach Contact vao file text.txt (luu tru ben vung)."""

    def __init__(self, file_path: str = "text.txt"):
        self.file_path = file_path
        self._ensure_file()

    # ------------------------------------------------------------------
    def _ensure_file(self) -> None:
        """
        Neu text.txt CHUA TUNG TON TAI (lan chay dau tien), tao file kem theo
        vai du lieu mau de demo cac chuc nang (badge Favorite/Emergency,
        sap xep uu tien...) ngay khi vua mo chuong trinh.
        Neu file da ton tai (da chay truoc do), KHONG duoc ghi de/mat du
        lieu nguoi dung da luu (dung NFR-2 - Reliability).
        """
        if not os.path.exists(self.file_path):
            seed_contacts = [
                Contact(
                    contact_id=1, user_id=1, name="Nguyen Van An",
                    phone_number="0901234567", email="an.nguyen@gmail.com",
                    address="12 Nguyen Trai, Quan 5, TP.HCM",
                    is_favorite=True, is_emergency=False,
                ),
                Contact(
                    contact_id=2, user_id=1, name="Tran Thi Bich",
                    phone_number="0912345678", email="bich.tran@gmail.com",
                    address="45 Le Loi, Quan 1, TP.HCM",
                    is_favorite=False, is_emergency=True,
                ),
                Contact(
                    contact_id=3, user_id=1, name="Le Hoang Chau",
                    phone_number="0987654321", email="",
                    address="",
                    is_favorite=False, is_emergency=False,
                ),
            ]
            self.save_all(seed_contacts)

    # ------------------------------------------------------------------
    def load_all(self) -> List[Contact]:
        """
        Doc toan bo contact tu text.txt.
        Neu mot dong bi hong (vi du: file bi sua tay sai dinh dang), dong do
        se bi BO QUA thay vi lam crash toan bo chuong trinh - dam bao du
        lieu con lai khong bi anh huong (NFR-2: "input errors occur, the
        system must not corrupt previously stored data").
        """
        contacts: List[Contact] = []
        if not os.path.exists(self.file_path):
            return contacts
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    contacts.append(Contact.from_dict(data))
                except (json.JSONDecodeError, KeyError, ValueError):
                    print(f"[Canh bao] Bo qua dong du lieu loi so {line_number} "
                          f"trong file {self.file_path}")
        return contacts

    # ------------------------------------------------------------------
    def save_all(self, contacts: List[Contact]) -> None:
        """
        Ghi TOAN BO danh sach contact xuong text.txt.
        Ky thuat "atomic write": ghi ra file tam (.tmp) truoc, ghi thanh cong
        het roi moi doi ten de thay the file that. Nho vay, neu chuong trinh
        bi tat dot ngot (mat dien, crash...) dung luc dang ghi, file text.txt
        goc VAN GIU NGUYEN du lieu cu, khong bi hong nua chung (NFR-2).
        """
        tmp_path = self.file_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            for contact in contacts:
                f.write(json.dumps(contact.to_dict(), ensure_ascii=False) + "\n")
        os.replace(tmp_path, self.file_path)

    # ------------------------------------------------------------------
    def get_next_id(self, contacts: List[Contact]) -> int:
        """Sinh contact_id ke tiep (tu tang, mo phong AUTO_INCREMENT)."""
        if not contacts:
            return 1
        return max(c.contact_id for c in contacts) + 1
