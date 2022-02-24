from domonic.html import *
from customer import User, CustomerProfile

class HtmlGenerator:
    def __init__(self, profile: CustomerProfile):
        if profile is None:
            raise Exception("Profile must be defined for a Render")
        self.profile = profile

        self.html = html(self.get_head(), self.get_body())

    
    # lol
    def get_head(self):
        return head(
            style(),
            script()
        )


    def get_body(self):
        return body(
            h1("Social Media Niche Market Research")
        )



class TopPostsCustomerProfileHtmlGenerator(HtmlGenerator):
    def __init__(self, profile: CustomerProfile):
        super().__init__(profile)



if __name__ == "__main__":
    user = User("Kobe the GoldenDoodle")
    customer = CustomerProfile(user, "mindmatterswithdiv")
    customer.follow_instagram_accounts("koberdoodle", "mindmatterswithdiv", "curly_therapist", "selfcare4yu")

    render = TopPostsCustomerProfileHtmlGenerator(customer)

    print(render.html)