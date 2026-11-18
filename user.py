class User:
    def __init__(self, name, password):
        self.__name = name
        self.__password = password

    @property
    def get_name(self):
        return self.__name