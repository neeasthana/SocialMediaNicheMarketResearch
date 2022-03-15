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
        self.sidecar_count = 0
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

            [body.appendChild(content) for content in self._rendered_content(post.asset)]

        body.appendChild(TopPostsCustomerProfileHtmlGenerator._inline_css_for_content_couresal())
        body.appendChild(TopPostsCustomerProfileHtmlGenerator._inline_javascript_for_content_couresal())

        return body


    def _rendered_content(self, content):
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
            self.sidecar_count = self.sidecar_count + 1

            rendered_content = [self._rendered_content(asset) for asset in content.content_list]
            
            # Reference: https://www.w3schools.com/howto/howto_js_slideshow.asp
            slideshow_div = div(_class="slideshow-container")
            dots_div = div(style="text-align:center")

            prev_button = a("&#10094;", _class="prev", onclick="plusSlides(-1)")
            next_button = a("&#10095;", _class="next", onclick="plusSlides(1)")

            for idx,content in enumerate(rendered_content):
                slides_div = div(_class="mySlides" + str(self.sidecar_count) + " fade")
                slides_div.appendChild(content)
                slideshow_div.appendChild(slides_div)
                dots_div.appendChild(span(_class="dot", onclick="currentSlide(" + str(idx + 1) + ")"))

            result.extend([slideshow_div, prev_button, next_button, dots_div])

        else:
            raise Exception("Cannot Render Unsupported Content Type: " + str(type(content)))
        

        return result


    def _inline_css_for_content_couresal():
        return style("""
            * {box-sizing:border-box}

            /* Slideshow container */
            .slideshow-container {
              max-width: 1000px;
              position: relative;
              margin: auto;
            }

            /* Hide the images by default */
            .mySlides {
              display: none;
            }

            /* Next & previous buttons */
            .prev, .next {
              cursor: pointer;
              position: absolute;
              top: 50%;
              width: auto;
              margin-top: -22px;
              padding: 16px;
              color: white;
              font-weight: bold;
              font-size: 18px;
              transition: 0.6s ease;
              border-radius: 0 3px 3px 0;
              user-select: none;
            }

            /* Position the "next button" to the right */
            .next {
              right: 0;
              border-radius: 3px 0 0 3px;
            }

            /* On hover, add a black background color with a little bit see-through */
            .prev:hover, .next:hover {
              background-color: rgba(0,0,0,0.8);
            }

            /* Caption text */
            .text {
              color: #f2f2f2;
              font-size: 15px;
              padding: 8px 12px;
              position: absolute;
              bottom: 8px;
              width: 100%;
              text-align: center;
            }

            /* Number text (1/3 etc) */
            .numbertext {
              color: #f2f2f2;
              font-size: 12px;
              padding: 8px 12px;
              position: absolute;
              top: 0;
            }

            /* The dots/bullets/indicators */
            .dot {
              cursor: pointer;
              height: 15px;
              width: 15px;
              margin: 0 2px;
              background-color: #bbb;
              border-radius: 50%;
              display: inline-block;
              transition: background-color 0.6s ease;
            }

            .active, .dot:hover {
              background-color: #717171;
            }

            /* Fading animation */
            .fade {
              -webkit-animation-name: fade;
              -webkit-animation-duration: 1.5s;
              animation-name: fade;
              animation-duration: 1.5s;
            }

            @-webkit-keyframes fade {
              from {opacity: .4}
              to {opacity: 1}
            }

            @keyframes fade {
              from {opacity: .4}
              to {opacity: 1}
            }
            """)


    def _inline_javascript_for_content_couresal():
        return script("""
            var slideIndex = [1,1];
            /* Class the members of each slideshow group with different CSS classes */
            var slideId = ["mySlides1", "mySlides2"]
            showSlides(1, 0);
            showSlides(1, 1);

            function plusSlides(n, no) {
              showSlides(slideIndex[no] += n, no);
            }

            function showSlides(n, no) {
              var i;
              var x = document.getElementsByClassName(slideId[no]);
              if (n > x.length) {slideIndex[no] = 1}
              if (n < 1) {slideIndex[no] = x.length}
              for (i = 0; i < x.length; i++) {
                x[i].style.display = "none";
              }
              x[slideIndex[no]-1].style.display = "block";
            }
            """)





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