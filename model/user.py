class User:
    """
    User Model
    """

    def __init__(self,
                 user_id,
                 full_name,
                 email,
                 phone,
                 password,
                 avatar=""):

        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password = password
        self.avatar = avatar

    def to_line(self):
        """
        Convert object -> txt
        """

        return f"{self.user_id}|{self.full_name}|{self.email}|{self.phone}|{self.password}|{self.avatar}"

    @staticmethod
    def from_line(line):
        """
        Convert txt -> object
        """

        data = line.strip().split("|")

        if len(data) < 5:
            return None

            # Nếu dòng dữ liệu chỉ có 5 phần (thiếu avatar), ta thêm một phần tử rỗng
        while len(data) < 6:
            data.append("")

        return User(
            int(data[0]),
            data[1],
            data[2],
            data[3],
            data[4],
            data[5]
        )

    def __str__(self):
        return f"{self.full_name} ({self.email})"