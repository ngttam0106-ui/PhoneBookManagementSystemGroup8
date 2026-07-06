# Phone Book Management System — Contact Module
### Nhom 8 — Doan Minh Khang — phan phu trach: Add / Edit / Delete / View Contact / Favorite / Emergency

Day la phan chuong trinh Python cho cac use case duoc phan cong:

| Use case (bao cao) | File cai dat | Trang thai |
|---|---|---|
| UC6 — Add Contact | `contact_manager.py` + `gui.py` (`AddContactWindow`) | Da xong |
| UC10 — View Contact Detail | `gui.py` (`ViewContactWindow`) | Da xong |
| UC11 — Edit Contact | `contact_manager.py` + `gui.py` (`EditContactWindow`) | Da xong |
| UC12 — Mark Special Contact (Favorite/Emergency) | `contact_manager.py` (`toggle_favorite`/`toggle_emergency`) | Da xong |
| UC13 — Delete Contact | `contact_manager.py` + `gui.py` (`ConfirmDialog`) | Da xong |

Cac use case KHAC (Register/Login/Logout/Update Profile — FR-1; Browse/Search/
Sort — FR-3; Contact Group — FR-4; Reset All — FR-5) **khong** thuoc pham vi
file nay, do cac thanh vien khac trong nhom phu trach.

---

## 1. Cai dat va chay chuong trinh

Yeu cau: Python 3.9+ (co san Tkinter — mac dinh co san tren Windows/macOS; tren
Linux neu thieu thi `sudo apt install python3-tk`).

```bash
# Cai thu vien duy nhat can them (de xu ly anh dai dien / avatar)
pip install pillow

# Chay chuong trinh
python main.py
```

Lan dau chay se tu dong tao file **`text.txt`** (dung dinh dang NFR-5 trong
bao cao) kem theo 3 lien he mau de xem thu giao dien. Cac lan chay sau se doc
lai dung du lieu da luu.

## 2. Kien truc code (khop voi DFD Process 2.0 & Class Diagram)

```
models.py              Lop Contact (thuc the / entity)
contact_repository.py  Doc/ghi text.txt (Data Access Layer)  -> D2 Contact Data
contact_manager.py      Nghiep vu: validate, chong trung SDT, -> Process 2.0
                        5 use case chinh                          Contact Management
avatar_utils.py         Sinh avatar hinh tron (anh that / chu cai dau)
gui.py                  Giao dien Tkinter (5 man hinh Muc VII bao cao)
main.py                 Diem chay chuong trinh
```

Kien truc 3 tang (Model — Repository — Manager) tach biet ro rang:
- **models.py**: chi la du lieu (khong logic).
- **contact_repository.py**: chi doc/ghi file, khong biet gi ve validate.
- **contact_manager.py**: toan bo logic nghiep vu (day la lop tuong ung
  "ContactManager"/"Process 2.0" trong so do), goi Repository de luu.
- **gui.py**: chi goi ham cua ContactManager va hien thi ket qua — khong tu
  xu ly du lieu truc tiep.

## 3. Diem can luu y khi ghep code voi nhom

- **Luu tru**: theo dung NFR-5, du lieu nam trong 1 file van ban `text.txt`
  (dang JSON Lines — moi dong 1 lien he). Khong dung MySQL/SQLite.
- **User dang nhap**: Module nay duoc code va kiem thu **doc lap**, nen
  `main.py` tam thoi gia lap san `user_id = 1` (xem hang so `DEMO_USER_ID`).
  Khi ghep voi module Dang nhap that cua nhom, chi can thay gia tri nay bang
  `user_id` lay tu phien dang nhap that (`ContactManager(user_id=...)`).
- **Danh sach lien he** (`gui.py` → `PhoneBookApp`) hien theo dung mockup:
  bam vao 1 dong se **mo rong ngay tai cho**, hien 3 nut **View | Edit |
  Delete** (chi 1 dong mo rong tai 1 thoi diem). Day chi la ban toi gian du
  de chon contact thao tac — chuc nang Browse/Search/Sort **day du**
  (UC7–UC9) la phan cua thanh vien khac; o ban nay chi co 1 o tim kiem don
  gian de tien dung/demo.
- **Nut tron "+" noi** o goc duoi phai danh sach: bam vao hien popup 2 dong
  "Create New Group" / "Add Contact" (dung mockup). "Add Contact" chay
  chuc nang that; **"Create New Group" chi la giao dien** (bam vao se bao
  ro day khong thuoc pham vi module nay) vi Contact Group Management (FR-4)
  la phan cua thanh vien khac.
- **Man hinh View KHONG con nut Message/Call/Video** (da bo hoan toan theo
  yeu cau — khong co FR nao yeu cau goi dien/nhan tin that).

## 4. Quy tac validate da cai dat

- **Name**: bat buoc.
- **Phone Number**: bat buoc, dung 10 chu so va bat dau bang so 0
  (vi du hop le: `0912345678`).
- **Email**: khong bat buoc, nhung neu nhap thi phai dung dang `xxx@xxx.xxx`.
- **So dien thoai trung**: kiem tra trong PHAM VI 1 user (dung Unique Key
  (user_id, phone_number) trong Data Model), thong bao ro ten lien he da
  dang dung so do.

## 5. Kiem thu

Toan bo 5 use case da duoc kiem thu (logic nghiep vu + tuong tac giao dien)
truoc khi ban giao. Bang Test Case chi tiet nam trong file rieng
`Testing_Document_Phone_Book_Contact_Module.xlsx` (dung dung template
"Testing Document Template" tu Elearning).
