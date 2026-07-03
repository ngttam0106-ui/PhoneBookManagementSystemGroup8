class User:

    def __init__(self, user_id, full_name, phone, email, password, avatar=""):
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.password = password
        self.avatar = avatar