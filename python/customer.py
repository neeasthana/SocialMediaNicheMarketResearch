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
        self.instagram_profile = InstagramAccount(instagram_username)
        self.follwing_accounts = []


    def follow_instagram_accounts(self, *instagram_handles):
        for handle in instagram_handles:
            account = InstagramAccount(handle)
            self.follwing_accounts.append(account)



if __name__ == "__main__":
    user = User("Kobe the GoldenDoodle")
    customer = CustomerProfile(user, "mindmatterswithdiv")
    customer.follow_instagram_accounts("mindmatterswithdiv", "curly_therapist", "selfcare4yu")