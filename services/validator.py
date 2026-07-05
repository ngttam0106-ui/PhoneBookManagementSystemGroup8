import re

class Validator:

    @staticmethod
    def validate_email(email):

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if re.match(pattern, email):
            return True

        return False

    @staticmethod
    def validate_phone(phone):

        pattern = r'^0\d{9}$'

        if re.match(pattern, phone):
            return True

        return False

    @staticmethod
    def validate_password(password):

        if len(password) < 6:
            return False

        return True