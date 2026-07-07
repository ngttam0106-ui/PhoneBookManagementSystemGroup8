from services.file_manager import FileManager
from model.contact import Contact


class ContactService:
    def __init__(self, current_user=None):
        self.file_manager = FileManager()
        self.current_user = current_user
        self.contacts = self.file_manager.load_contacts()

    def _current_user_contacts(self):
        if self.current_user is None:
            return self.contacts

        return [
            contact for contact in self.contacts
            if getattr(contact, "user_id", None) == self.current_user.user_id
        ]

    def _save_contacts(self):
        self.file_manager.save_contacts(self.contacts)

    def is_duplicate_contact(self, name, phone, email, address, exclude_id=None):
        normalized = lambda value: (value or "").strip().lower()
        name = normalized(name)
        phone = (phone or "").strip()
        email = normalized(email)
        address = normalized(address)

        for contact in self._current_user_contacts():
            if exclude_id is not None and contact.contact_id == exclude_id:
                continue

            if (
                normalized(contact.name) == name
                and (contact.phone or "").strip() == phone
                and normalized(contact.email) == email
                and normalized(contact.address) == address
            ):
                return True

        return False

    def add_contact(self, name, phone, email, address="", avatar="", favorite=False, emergency=False):
        if self.is_duplicate_contact(name, phone, email, address):
            return None

        if len(self.contacts) == 0:
            new_id = 1
        else:
            new_id = max(contact.contact_id for contact in self.contacts) + 1

        user_id = self.current_user.user_id if self.current_user else 0

        contact = Contact(
            contact_id=new_id,
            user_id=user_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
            avatar=avatar,
            favorite=favorite,
            emergency=emergency
        )

        self.contacts.append(contact)
        self._save_contacts()
        return contact

    def edit_contact(self, contact_id, name=None, phone=None, email=None, address=None, avatar=None,
                     favorite=None, emergency=None):
        contact = self.get_contact(contact_id)

        if contact is None:
            return False

        new_name = name if name is not None else contact.name
        new_phone = phone if phone is not None else contact.phone
        new_email = email if email is not None else contact.email
        new_address = address if address is not None else contact.address

        if self.is_duplicate_contact(new_name, new_phone, new_email, new_address, exclude_id=contact_id):
            return False

        if name is not None:
            contact.name = name
        if phone is not None:
            contact.phone = phone
        if email is not None:
            contact.email = email
        if address is not None:
            contact.address = address
        if avatar is not None:
            contact.avatar = avatar
        if favorite is not None:
            contact.favorite = favorite
        if emergency is not None:
            contact.emergency = emergency

        self._save_contacts()
        return True

    def delete_contact(self, contact_id):
        original_len = len(self.contacts)
        self.contacts = [contact for contact in self.contacts if contact.contact_id != contact_id]

        if len(self.contacts) != original_len:
            self._save_contacts()
            return True

        return False

    def get_contact(self, contact_id):
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                return contact
        return None

    def get_all_contacts(self):
        return self._current_user_contacts()

    def get_favorite_contacts(self):
        return [
            contact for contact in self._current_user_contacts()
            if getattr(contact, "favorite", False)
        ]

    def get_emergency_contacts(self):
        return [
            contact for contact in self._current_user_contacts()
            if getattr(contact, "emergency", False)
        ]

    def search_contact(self, keyword):
        result = []
        keyword = keyword.lower()

        for contact in self._current_user_contacts():
            if (
                keyword in contact.name.lower()
                or keyword in contact.phone
                or (contact.email and keyword in contact.email.lower())
            ):
                result.append(contact)

        return result

    def sort_latest(self):
        return sorted(self._current_user_contacts(), key=lambda contact: contact.contact_id, reverse=True)

    def sort_oldest(self):
        return sorted(self._current_user_contacts(), key=lambda contact: contact.contact_id)

    def sort_az(self):
        return sorted(self._current_user_contacts(), key=lambda contact: contact.name.lower())

    def mark_favorite(self, contact_id):
        contact = self.get_contact(contact_id)

        if contact is None:
            return False

        contact.favorite = not contact.favorite
        self._save_contacts()
        return True

    def mark_emergency(self, contact_id):
        contact = self.get_contact(contact_id)

        if contact is None:
            return False

        contact.emergency = not contact.emergency
        self._save_contacts()
        return True

    def reset_all_contacts(self):
        self.contacts = []
        self._save_contacts()
        return True