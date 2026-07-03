class Contact:

    def __init__(self,
                 contact_id,
                 user_id,
                 name,
                 phone,
                 email,
                 address,
                 avatar="",
                 favorite=False,
                 emergency=False):

        self.contact_id = contact_id
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.avatar = avatar
        self.favorite = favorite
        self.emergency = emergency