from user import User

class Admin(User):
    def __init__(self, name, password, sign):
        super().__init__(name, password)
        self.__sign = sign

    @property
    def get_sign(self):
        return self.__sign
