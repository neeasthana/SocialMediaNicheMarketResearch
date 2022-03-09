from domonic.html import *
from customer import User, CustomerProfile
from accounts import InstagramPost
from retriever import ContentRetriever
from content import *
import os
import requests


retriever = ContentRetriever()


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
        _create_cache_folder()


    def get_body(self):
        body = super().get_body()

        most_liked_posts = [(account, account.get_most_liked_post()) for account in self.profile.follwing_accounts]

        for account, post in most_liked_posts:
            header = h2(account.username)
            likes = h3("Likes: " + str(post.likes))
            comments = h3("Comments: " + str(post.comments))
            # image = img(src=retriever.file_location(content_url))

            body.appendChild(header)
            body.appendChild(likes)
            body.appendChild(comments)

            [body.appendChild(content) for content in TopPostsCustomerProfileHtmlGenerator._rendered_content(post.asset)]

        return body


    def _rendered_content(content):
        result = []

        if type(content) is InstagramVideoContent:
            content_url = content.content_url()
            retriever.retrieve(content_url)
            html_video = video(type= "video/mp4", crossorigin="anonymous", src = retriever.file_location(content_url))
            result.append(html_video)

        elif type(content) is InstagramPhotoContent:
            content_url = content.content_url()
            retriever.retrieve(content_url)
            image = img(src=retriever.file_location(content_url))
            result.append(image)

        elif type(content) is InstagramSidecarContent:
            rendered_content = [TopPostsCustomerProfileHtmlGenerator._rendered_content(asset) for asset in content.content_list]
            result.extend(rendered_content)

        else:
            raise Exception("Cannot Render Unsupported Content Type: " + str(type(content)))
        

        return result





#Ref: https://www.geeksforgeeks.org/download-instagram-profile-pic-using-python/
def download_instagram_image(post: InstagramPost):
    filename = instagram_post_cache_location(post)
    file_exists = os.path.isfile(filename)
 
    if not file_exists:
        with open(filename, 'wb') as handle:
            response = requests.get(post.url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)


CACHE_LOCATION = os.path.join(os.getcwd(),".cache/content")

def _create_cache_folder():
    path = CACHE_LOCATION
    if not os.path.exists(path):
        os.mkdir(path)


def instagram_post_cache_location(post: InstagramPost):
    return CACHE_LOCATION + "/" + instagram_post_to_filename(post)


def instagram_post_to_filename(post: InstagramPost):
    return post.url.split("?")[0].replace("https://", "").split("/")[-1]



if __name__ == "__main__":
    user = User("Kobe the GoldenDoodle")
    customer = CustomerProfile(user, "mindmatterswithdiv")
    customer.follow_instagram_accounts("millennial.therapist", "holisticallygrace", "curly_therapist", "selfcare4yu", "thebraincoach")

    render = TopPostsCustomerProfileHtmlGenerator(customer)

    render.save()