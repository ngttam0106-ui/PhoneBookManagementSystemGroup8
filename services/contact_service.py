from services.file_manager import FileManager
class ContactService:
    def __init__(self):
        self.file_manager = FileManager()
        self.contacts = self.file_manager.load_contacts()
    def add_contact(self):
        pass

    def edit_contact(self):
        pass

    def delete_contact(self):
        pass

    def get_contact(self):
        pass

    def get_all_contacts(self):
        pass

    def search_contact(self, keyword):
        result = []

        keyword = keyword.lower()

        for contact in self.contacts:
            if (keyword in contact.name.lower()
                    or keyword in contact.phone
                    or keyword in contact.email.lower()):
                result.append(contact)

        return result

    def sort_latest(self):
        self.contacts.sort(
            key=lambda contact: contact.contact_id,
            reverse=True
        )
        return self.contacts

    def sort_oldest(self):
        self.contacts.sort(
            key=lambda contact: contact.contact_id
        )
        return self.contacts

    def sort_az(self):
        self.contacts.sort(
            key=lambda contact: contact.lower()
        )
        return self.contacts

    def mark_favorite(self):
        pass

    def mark_emergency(self):
        pass

    def reset_all_contacts(self):
        pass
    def get_all_contacts(self):
        return self.contacts