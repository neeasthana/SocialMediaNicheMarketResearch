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


    def save(self, filename = "report.html"):
        with open(filename, "w") as f:
            f.write(str(self.html))



class TopPostsCustomerProfileHtmlGenerator(HtmlGenerator):
    def __init__(self, profile: CustomerProfile):
        super().__init__(profile)


    def get_body(self):
        body = super().get_body()

        most_liked_posts = [(account, account.get_most_liked_post()) for account in self.profile.follwing_accounts]

        for account, post in most_liked_posts:
            header = h2(account.username)
            likes = h3("Likes: " + str(post.likes))
            comments = h3("Comments: " + str(post.comments))
            image = img(src=post.url, alt = "a post picture", crossorigin="anonymous")
            body.appendChild(header)
            body.appendChild(likes)
            body.appendChild(comments)
            body.appendChild(image)

        return body




if __name__ == "__main__":
    user = User("Kobe the GoldenDoodle")
    customer = CustomerProfile(user, "mindmatterswithdiv")
    customer.follow_instagram_accounts("koberdoodle", "mindmatterswithdiv", "curly_therapist", "selfcare4yu", "oregonfootball")

    render = TopPostsCustomerProfileHtmlGenerator(customer)

    render.save()