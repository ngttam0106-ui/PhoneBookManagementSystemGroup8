from model.user import User
from services.file_manager import FileManager
from services.validator import Validator
from services.security import Security


class AuthService:

    @staticmethod
    def generate_user_id():

        users = FileManager.load_users()

        if len(users) == 0:
            return 1

        max_id = max(int(user.user_id) for user in users)

        return max_id + 1


    @staticmethod
    def email_exists(email):

        users = FileManager.load_users()

        for user in users:

            if user.email.lower() == email.lower():
                return True

        return False


    @staticmethod
    def phone_exists(phone):

        users = FileManager.load_users()

        for user in users:

            if user.phone == phone:
                return True

        return False


    @staticmethod
    def register(full_name,
                 email,
                 phone,
                 password,
                 confirm_password):

        # Empty

        if Validator.is_empty(full_name):
            return False, "Full name is required."

        if Validator.is_empty(email):
            return False, "Email is required."

        if Validator.is_empty(phone):
            return False, "Phone number is required."

        if Validator.is_empty(password):
            return False, "Password is required."

        # Validate

        if not Validator.is_valid_email(email):
            return False, "Invalid email."

        if not Validator.is_valid_phone(phone):
            return False, "Phone number must contain 10 digits."

        if not Validator.is_valid_password(password):
            return False, "Password must be at least 6 characters."

        if not Validator.is_same_password(password,
                                          confirm_password):

            return False, "Password confirmation does not match."

        # Duplicate

        if AuthService.email_exists(email):
            return False, "Email already exists."

        if AuthService.phone_exists(phone):
            return False, "Phone number already exists."

        # Create User

        user = User(
            AuthService.generate_user_id(),
            full_name,
            email,
            phone,
           Security.hash_password(password),
            ""
        )

        FileManager.append_user(user)

        return True, "Register successfully."


    @staticmethod
    def login(email,
              password):

        users = FileManager.load_users()

        for user in users:

            if user.email.lower() == email.lower() \
                     and Security.verify_password(
                          password,
                          user.password 
                          ):

                return True, user

        return False, None


    @staticmethod
    def update_profile(user_id,
                       full_name,
                       phone,
                       avatar):

        users = FileManager.load_users()

        for user in users:

            if int(user.user_id) == int(user_id):

                # Duplicate phone

                for other in users:

                    if other.user_id != user.user_id:

                        if other.phone == phone:

                            return False, "Phone number already exists."

                if Validator.is_empty(full_name):
                    return False, "Full name is required."

                if not Validator.is_valid_phone(phone):
                    return False, "Invalid phone number."

                user.full_name = full_name
                user.phone = phone
                user.avatar = avatar

                FileManager.save_users(users)

                return True, "Profile updated."

        return False, "User not found."