import uuid

class CustomerProfile:
    def __init__(self, user: User, instagram_username = None):
        self.user = user


class User:
    """
    Placeholder class to represent a user and their authentication with our site 
    """
    def __init__(self, username):
        self.username = username
        self.id = uuid.uuid1()