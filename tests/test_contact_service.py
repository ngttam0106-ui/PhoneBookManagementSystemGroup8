import os
import tempfile
import unittest

from services.contact_service import ContactService
from services.file_manager import FileManager


class DummyUser:
    def __init__(self, user_id=1):
        self.user_id = user_id


class ContactServiceTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.contacts_file = os.path.join(self.temp_dir.name, "contacts.txt")
        self.groups_file = os.path.join(self.temp_dir.name, "groups.txt")
        self.mapping_file = os.path.join(self.temp_dir.name, "mapping.txt")
        self.users_file = os.path.join(self.temp_dir.name, "users.txt")

        FileManager.CONTACT_FILE = self.contacts_file
        FileManager.GROUP_FILE = self.groups_file
        FileManager.MAPPING_FILE = self.mapping_file
        FileManager.USER_FILE = self.users_file

    def test_add_toggle_and_edit_contact(self):
        service = ContactService(current_user=DummyUser())

        contact = service.add_contact(
            name="Alice",
            phone="0123456789",
            email="alice@example.com"
        )

        self.assertEqual(contact.contact_id, 1)

        self.assertTrue(service.mark_favorite(contact.contact_id))
        self.assertTrue(service.get_contact(contact.contact_id).favorite)

        self.assertTrue(service.mark_emergency(contact.contact_id))
        self.assertTrue(service.get_contact(contact.contact_id).emergency)

        self.assertTrue(
            service.edit_contact(
                contact.contact_id,
                name="Alice Updated",
                phone="0999999999"
            )
        )

        updated = service.get_contact(contact.contact_id)
        self.assertEqual(updated.name, "Alice Updated")
        self.assertEqual(updated.phone, "0999999999")

    def test_delete_contact(self):
        service = ContactService(current_user=DummyUser())

        contact = service.add_contact(
            name="Bob",
            phone="1111111111",
            email="bob@example.com"
        )

        self.assertTrue(service.delete_contact(contact.contact_id))
        self.assertIsNone(service.get_contact(contact.contact_id))


if __name__ == "__main__":
    unittest.main()
