# -*- coding: utf-8 -*-
"""
contact_manager.py
-------------------
Tang nghiep vu (Business Logic Layer), tuong ung voi "Process 2.0 - Contact
Management" trong so do DFD muc dinh (Muc III.2.2 bao cao).

Lop ContactManager cai dat DAY DU 5 use case thuoc pham vi phu trach:
    UC6  - Add Contact
    UC10 - View Contact Detail
    UC11 - Edit Contact
    UC12 - Mark Special Contact (Favorite / Emergency)
    UC13 - Delete Contact

NGUYEN TAC BAO MAT (NFR-4): "Users are not allowed to access or modify other
users' data" -> MOI thao tac doc/sua/xoa deu duoc loc theo self.user_id
(nguoi dung dang dang nhap hien tai). ContactManager KHONG tu xac thuc user -
user_id duoc truyen vao tu module Dang nhap (Account Management, FR-1, do
thanh vien khac trong nhom phu trach).
"""

from __future__ import annotations
import re
from typing import List, Optional, Tuple

from models import Contact
from contact_repository import ContactRepository


# So dien thoai Viet Nam: dung 10 chu so, bat dau bang so 0
PHONE_REGEX = re.compile(r"^0\d{9}$")
# Email co ban dang xxx@xxx.xxx
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ContactManager:
    """Xu ly nghiep vu quan ly Contact cho MOT user dang dang nhap."""

    def __init__(self, user_id: int, repository: Optional[ContactRepository] = None):
        self.user_id = user_id
        self.repository = repository or ContactRepository()

    # ------------------------------------------------------------------
    # Truy van danh sach / chi tiet (phuc vu UC10 - View Contact Detail;
    # phan Browse/Search/Sort day du la FR-3, do thanh vien khac phu trach -
    # o day chi lam vua du de chon duoc contact can Xem/Sua/Xoa)
    # ------------------------------------------------------------------
    def get_all_contacts(self) -> List[Contact]:
        """
        Tra ve danh sach contact CUA RIENG user hien tai (NFR-4), da sap xep
        theo thu tu uu tien: Emergency -> Favorite -> A-Z (dap ung yeu cau
        "priority display" trong FR-2).
        """
        all_contacts = self.repository.load_all()
        mine = [c for c in all_contacts if c.user_id == self.user_id]
        mine.sort(key=lambda c: c.priority_rank)
        return mine

    def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        UC10 - View Contact Detail: lay 1 contact theo ID.
        CHI tra ve neu contact thuoc ve user hien tai; nguoc lai tra ve None
        (khong cho xem du lieu cua user khac - NFR-4).
        """
        for c in self.get_all_contacts():
            if c.contact_id == contact_id:
                return c
        return None

    # ------------------------------------------------------------------
    # Validate du lieu dau vao (dung chung cho Add & Edit)
    # ------------------------------------------------------------------
    @staticmethod
    def validate_name(name: str) -> Optional[str]:
        if not name or not name.strip():
            return "Full name is required."
        return None

    @staticmethod
    def validate_phone_format(phone: str) -> Optional[str]:
        if not phone or not phone.strip():
            return "Phone number is required."
        if not PHONE_REGEX.match(phone.strip()):
            return "Invalid phone number. It must contain exactly 10 digits and start with 0."
        return None

    @staticmethod
    def validate_email_format(email: str) -> Optional[str]:
        # Email khong bat buoc (UC6: chi Name & Phone Number la required)
        if email and not EMAIL_REGEX.match(email.strip()):
            return "Invalid email format."
        return None

    def find_duplicate(self, phone: str, exclude_id: Optional[int] = None) -> Optional[Contact]:
        """
        Kiem tra trung so dien thoai TRONG PHAM VI user hien tai, dung Unique
        Key (user_id, phone_number) mo ta o Muc VI Data Model.
        exclude_id: bo qua chinh contact dang duoc sua (tranh bao trung voi
        chinh no khi Edit ma khong doi so dien thoai).
        """
        phone = phone.strip()
        for c in self.get_all_contacts():
            if exclude_id is not None and c.contact_id == exclude_id:
                continue
            if c.phone_number == phone:
                return c
        return None

    # ------------------------------------------------------------------
    # UC6 - Add Contact
    # ------------------------------------------------------------------
    def add_contact(
        self, name: str, phone_number: str, email: str = "",
        address: str = "", avatar_path: str = "",
    ) -> Tuple[bool, str, Optional[Contact]]:
        """
        Buoc 3-4 (UC6): validate cac truong bat buoc (Name, Phone Number) va
        dinh dang du lieu; kiem tra trung so dien thoai.
        Buoc 5 (UC6): luu contact moi va cap nhat danh sach ngay lap tuc.
        Tra ve (thanh_cong, thong_diep, contact_moi_hoac_None).
        """
        name = (name or "").strip()
        phone_number = (phone_number or "").strip()
        email = (email or "").strip()
        address = (address or "").strip()

        error = (
            self.validate_name(name)
            or self.validate_phone_format(phone_number)
            or self.validate_email_format(email)
        )
        if error:
            return False, error, None

        duplicate = self.find_duplicate(phone_number)
        if duplicate:
            return False, (
                f"This phone number is already used by another contact "
                f"('{duplicate.name}') in your phonebook."
            ), None

        all_contacts = self.repository.load_all()
        new_id = self.repository.get_next_id(all_contacts)
        new_contact = Contact(
            contact_id=new_id, user_id=self.user_id, name=name,
            phone_number=phone_number, email=email, address=address,
            avatar_path=avatar_path,
        )
        all_contacts.append(new_contact)
        self.repository.save_all(all_contacts)
        return True, "Contact added successfully.", new_contact

    # ------------------------------------------------------------------
    # UC11 - Edit Contact
    # ------------------------------------------------------------------
    def edit_contact(
        self, contact_id: int, name: str, phone_number: str,
        email: str = "", address: str = "", avatar_path: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Buoc 4 (UC11): validate du lieu, ghi de thong tin cu bang thong tin
        moi neu hop le. avatar_path=None nghia la "khong doi anh dai dien
        hien co"; truyen chuoi (ke ca chuoi rong) neu muon cap nhat/xoa anh.
        """
        name = (name or "").strip()
        phone_number = (phone_number or "").strip()
        email = (email or "").strip()
        address = (address or "").strip()

        error = (
            self.validate_name(name)
            or self.validate_phone_format(phone_number)
            or self.validate_email_format(email)
        )
        if error:
            return False, error

        duplicate = self.find_duplicate(phone_number, exclude_id=contact_id)
        if duplicate:
            return False, (
                f"This phone number is already used by another contact "
                f"('{duplicate.name}') in your phonebook."
            )

        all_contacts = self.repository.load_all()
        for c in all_contacts:
            if c.contact_id == contact_id and c.user_id == self.user_id:
                c.name = name
                c.phone_number = phone_number
                c.email = email
                c.address = address
                if avatar_path is not None:
                    c.avatar_path = avatar_path
                self.repository.save_all(all_contacts)
                return True, "Contact updated successfully."
        return False, "Contact not found."

    # ------------------------------------------------------------------
    # UC13 - Delete Contact
    # (Buoc xac nhan "Confirm Delete" <<include>> do lop giao dien - GUI -
    # dam nhiem thong qua ConfirmDialog, truoc khi goi ham nay)
    # ------------------------------------------------------------------
    def delete_contact(self, contact_id: int) -> Tuple[bool, str]:
        all_contacts = self.repository.load_all()
        remaining = [
            c for c in all_contacts
            if not (c.contact_id == contact_id and c.user_id == self.user_id)
        ]
        if len(remaining) == len(all_contacts):
            return False, "Contact not found."
        self.repository.save_all(remaining)
        return True, "Contact deleted successfully."

    # ------------------------------------------------------------------
    # UC12 - Mark Special Contact (Favorite / Emergency)
    # ------------------------------------------------------------------
    def toggle_favorite(self, contact_id: int) -> Tuple[bool, str, bool]:
        """Bat/tat nhan 'Favorite'. Tra ve (thanh_cong, thong_diep, trang_thai_moi)."""
        return self._toggle_flag(contact_id, "is_favorite", "Favorite")

    def toggle_emergency(self, contact_id: int) -> Tuple[bool, str, bool]:
        """Bat/tat nhan 'Emergency'. Tra ve (thanh_cong, thong_diep, trang_thai_moi)."""
        return self._toggle_flag(contact_id, "is_emergency", "Emergency")

    def _toggle_flag(self, contact_id: int, attr: str, label: str) -> Tuple[bool, str, bool]:
        all_contacts = self.repository.load_all()
        for c in all_contacts:
            if c.contact_id == contact_id and c.user_id == self.user_id:
                new_value = not getattr(c, attr)
                setattr(c, attr, new_value)
                self.repository.save_all(all_contacts)
                state = "marked as" if new_value else "removed from"
                return True, f"Contact {state} {label}.", new_value
        return False, "Contact not found.", False
