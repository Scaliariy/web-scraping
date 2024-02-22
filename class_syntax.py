class User:
    def __init__(self, name, birthyear):
        self.name = name
        self.birthyear = birthyear

    def get_name(self):
        return self.name.upper()

    def age(self, current_year):
        return current_year - self.birthyear


user = User("Nikolay", 2001)
print(user.age(2023))
print(user.get_name())
