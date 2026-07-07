from services.file_manager import FileManager
from model.group import Group
from model.contact_group import ContactGroup


class GroupService:

    def __init__(self):

        self.file_manager = FileManager()

        self.groups = self.file_manager.load_groups()
        self.mappings = self.file_manager.load_mapping()
        self.contacts = self.file_manager.load_contacts()

    # =====================================================

    def create_group(self, user_id, group_name):

        if len(self.groups) == 0:
            new_id = 1
        else:
            new_id = max(group.group_id for group in self.groups) + 1

        group = Group(
            group_id=new_id,
            user_id=user_id,
            group_name=group_name
        )

        self.groups.append(group)

        self.file_manager.save_groups(self.groups)

        return group

    # =====================================================

    def update_group(self, group_id, new_name):

        for group in self.groups:

            if group.group_id == group_id:

                group.group_name = new_name

                self.file_manager.save_groups(self.groups)

                return True

        return False

    # =====================================================

    def delete_group(self, group_id):

        self.groups = [
            group
            for group in self.groups
            if group.group_id != group_id
        ]

        self.mappings = [
            mapping
            for mapping in self.mappings
            if mapping.group_id != group_id
        ]

        self.file_manager.save_groups(self.groups)
        self.file_manager.save_mapping(self.mappings)

        return True

    # =====================================================

    def add_contact_to_group(self, contact_id, group_id):

        # Không cho thêm trùng
        for mapping in self.mappings:

            if (
                mapping.contact_id == contact_id
                and mapping.group_id == group_id
            ):
                return False

        if len(self.mappings) == 0:
            new_id = 1
        else:
            new_id = max(
                mapping.mapping_id
                for mapping in self.mappings
            ) + 1

        mapping = ContactGroup(
            mapping_id=new_id,
            contact_id=contact_id,
            group_id=group_id
        )

        self.mappings.append(mapping)

        self.file_manager.save_mapping(self.mappings)

        return True

    # =====================================================

    def remove_contact_from_group(self, contact_id, group_id):

        self.mappings = [

            mapping

            for mapping in self.mappings

            if not (

                mapping.contact_id == contact_id
                and mapping.group_id == group_id

            )

        ]

        self.file_manager.save_mapping(self.mappings)

        return True

    # =====================================================

    def get_group_contacts(self, group_id):

        contacts = []

        for mapping in self.mappings:

            if mapping.group_id == group_id:

                for contact in self.contacts:

                    if contact.contact_id == mapping.contact_id:

                        contacts.append(contact)

                        break

        return contacts

    # =====================================================

    def refresh(self):

        self.groups = self.file_manager.load_groups()
        self.mappings = self.file_manager.load_mapping()
        self.contacts = self.file_manager.load_contacts()