from domonic.html import *
from customer import User, CustomerProfile
from accounts import InstagramPost, InstagramAccount
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



class InstagramPostHtmlGenerator():
    def __init__(self, account: InstagramAccount, post: InstagramPost, body, sidecar_count):
        self.account = account
        self.post = post
        self.sidecar_count = sidecar_count


    def _append_html(self, body):
        header = h2(self.account.username)
        likes = h3("Likes: " + str(self.post.likes))
        comments = h3("Comments: " + str(self.post.comments))
        # image = img(src=retriever.file_location(content_url))info

        body.appendChild(header)
        body.appendChild(likes)
        body.appendChild(comments)

        [body.appendChild(content) for content in self._rendered_content(self.post.asset)]


    def render_html(self):
        post_div = div(_class="post")

        post_div.appendChild(self._render_header())

        post_div.appendChild(self._rendered_content(self.post.asset))

        post_div.appendChild(self._render_like_bar())

        post_div.appendChild(self._render_comments())

        return post_div


    def _render_header(self):
        info_div = div(_class="info")

        user_div = div(_class="user")

        profile_div = div(_class="profile-pic")
        profile_div.appendChild(img(src="assets/smile.PNG", alt=""))
        user_div.appendChild(profile_div)

        user_div.appendChild(p(self.account.username, _class="username"))

        info_div.appendChild(user_div)

        return info_div


    def _render_like_bar(self):
        post_content_div = div(_class="post-content")

        reaction_wrapper_div = div(_class="reaction-wrapper")
        reaction_wrapper_div.appendChild(img(src="assets/like.PNG", _class="icon", alt=""))
        reaction_wrapper_div.appendChild(img(src="assets/comment.PNG", _class="icon", alt=""))
        reaction_wrapper_div.appendChild(img(src="assets/send.PNG", _class="icon", alt=""))
        reaction_wrapper_div.appendChild(img(src="assets/save.PNG", _class="save icon", alt=""))
        post_content_div.appendChild(reaction_wrapper_div)

        post_content_div.appendChild(p(str(self.post.likes) + " likes", _class="likes"))

        caption = "<span>" + self.account.username + " </span>" + str(self.post.caption)
        post_content_div.appendChild(p(caption, _class="description"))

        post_content_div.appendChild(p(str(self.post.post_time), _class="post-time"))

        return post_content_div


    def _render_comments(self):
        comment_wrapper_div = div(_class="comment-wrapper")

        comment_wrapper_div.appendChild(img(src="assets/smile.PNG", _class="icon", alt=""))
        comment_wrapper_div.appendChild(input(type="text", _class="comment-box", placeholder="Add a comment"))
        comment_wrapper_div.appendChild(button("post", _class="comment-btn"))

        return comment_wrapper_div




    def _rendered_content(self, content):
        result = []

        if type(content) is InstagramVideoContent:
            content_url = content.content_url()
            retriever.retrieve(content_url)
            html_video = video(type= "video/mp4", crossorigin="anonymous", src = retriever.file_location(content_url), _class="post-image", alt="")
            result.append(html_video)

        elif type(content) is InstagramPhotoContent:
            content_url = content.content_url()
            retriever.retrieve(content_url)
            image = img(src=retriever.file_location(content_url), _class="post-image", alt="")
            result.append(image)

        elif type(content) is InstagramSidecarContent:
            rendered_content = [self._rendered_content(asset) for asset in content.content_list]
            
            # Reference: https://www.w3schools.com/howto/howto_js_slideshow.asp
            slideshow_div = div(_class="slideshow-container")
            dots_div = div(style="text-align:center")

            prev_button = a("&#10094;", _class="prev", onclick="plusSlides(-1," + str(self.sidecar_count-1) +")")
            next_button = a("&#10095;", _class="next", onclick="plusSlides(1," + str(self.sidecar_count-1) +")")

            for idx,content in enumerate(rendered_content):
                slides_div = div(_class="mySlides" + str(self.sidecar_count) + " fade")
                slides_div.appendChild(content)
                slideshow_div.appendChild(slides_div)
                dots_div.appendChild(span(_class="dot", onclick="currentSlide(" + str(idx + 1) + ")"))

            result.extend([slideshow_div, prev_button, next_button, dots_div])

        else:
            raise Exception("Cannot Render Unsupported Content Type: " + str(type(content)))
        

        return result





class TopPostsCustomerProfileHtmlGenerator(HtmlGenerator):
    def __init__(self, profile: CustomerProfile):
        self.sidecar_count = 0
        super().__init__(profile)
        _create_cache_folder()


    def get_body(self):
        body = super().get_body()

        most_liked_posts = [(account, account.get_most_liked_post()) for account in self.profile.follwing_accounts]

        for account, post in most_liked_posts:
            if type(post.asset) is InstagramSidecarContent:
                self.sidecar_count = self.sidecar_count + 1

            post_html = InstagramPostHtmlGenerator(account, post, body, self.sidecar_count)

            body.appendChild(post_html.render_html())

        body.appendChild(TopPostsCustomerProfileHtmlGenerator._inline_css_for_content_couresal())
        body.appendChild(TopPostsCustomerProfileHtmlGenerator._inline_css_for_posts())
        body.appendChild(TopPostsCustomerProfileHtmlGenerator._inline_javascript_for_content_couresal())
        body.appendChild(self._dynamic_javascript_for_content_couresal())

        return body



    """
    Should generate something like this for 3 slide couresals

        ```
            var slideIndex = [4,4,4];
            /* Class the members of each slideshow group with different CSS classes */
            var slideId = ["mySlides1", "mySlides2", "myslides3"]
            showSlides(1, 0);
            showSlides(1, 1);
            showSlides(1, 2);
        ```
    """
    def _dynamic_javascript_for_content_couresal(self):
        slideIndex = [1] * self.sidecar_count
        slideIndexStr = "var slideIndex = " + str(slideIndex) + ";\n"

        slideIds = []
        showSlidesString = ""
        for idx in range(self.sidecar_count):
            showSlidesString += "showSlides(1, " + str(idx) + ")\n"
            slideIds.append("mySlides" + str(idx+1))

        slideIdsStr = "var slideId = " + str(slideIds) + ";\n"

        return script(slideIndexStr + slideIdsStr + showSlidesString)


    def _inline_css_for_posts():
        return style("""
            .post{
                width: auto;
                height: auto;
                background: #fff;
                border: 1px solid #dfdfdf;
                margin-top: 40px;
            }

            .info{
                width: 100%;
                height: 60px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 20px;
            }

            .info .username{
                width: auto;
                font-weight: bold;
                color: #000;
                font-size: 14px;
                margin-left: 10px;
            }

            .info .options{
                height: 10px;
                cursor: pointer;
            }

            .info .user{
                display: flex;
                align-items: center;
            }

            .info .profile-pic{
                height: 40px;
                width: 40px;
                padding: 0;
                background: none;
            }

            .info .profile-pic img{
                border: none;
            }

            .post-image{
                width: auto;
                height: auto;
                object-fit: cover;
            }

            .post-content{
                width: auto;
                padding: 20px;
            }

            .likes{
                font-weight: bold;
            }

            .description{
                margin: 10px 0;
                font-size: 14px;
                line-height: 20px;
            }

            .description span{
                font-weight: bold;
                margin-right: 10px;
            }

            .post-time{
                color: rgba(0, 0, 0, 0.5);
                font-size: 12px;
            }

            .comment-wrapper{
                width: 100%;
                height: 50px;
                border-radius: 1px solid #dfdfdf;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .comment-wrapper .icon{
                height: 30px;
            }

            .comment-box{
                width: 80%;
                height: 100%;
                border: none;
                outline: none;
                font-size: 14px;
            }

            .comment-btn,
            .action-btn{
                width: 70px;
                height: 100%;
                background: none;
                border: none;
                outline: none;
                text-transform: capitalize;
                font-size: 16px;
                color: rgb(0, 162, 255);
                opacity: 0.5;
            }

            .reaction-wrapper{
                width: 100%;
                height: 50px;
                display: flex;
                margin-top: -20px;
                align-items: center;
            }

            .reaction-wrapper .icon{
                height: 25px;
                margin: 0;
                margin-right: 20px;
            }

            .reaction-wrapper .icon.save{
                margin-left: auto;
            }
            """)


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
              width: auto;
              margin-top: -22px;
              padding: 16px;
              color: black;
              font-weight: bold;
              font-size: 100px;
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