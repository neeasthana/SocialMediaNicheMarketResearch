import uuid
from accounts import InstagramAccount



class User:
    """
    Placeholder class to represent a user and their authentication with our site 
    """
    def __init__(self, username):
        self.username = username
        self.id = uuid.uuid1()



class CustomerProfile:
    def __init__(self, user: User, instagram_username = None):
        self.user = user
        self.instagram = InstagramAccount(instagram_username)


user = User("Kobe the GoldenDoodle")
customer = CustomerProfile(user, "mindmatterswithdiv")