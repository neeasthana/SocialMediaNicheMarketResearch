from retriever import HTMLRetriever, CachedHTMLRetriever
from content import *
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding":"gzip, deflate", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
}


retriever = CachedHTMLRetriever()

class Account:
    def __init__(self, identifier, sitename):
        self.identifier = identifier
        self.sitename = sitename


    def _retreive_parsed_profile_page(self):
        url = self._generate_account_url()
        response = retriever.retrieve(url)
        return BeautifulSoup(response, 'html.parser')


    def _generate_account_url(self):
        return "https://www." + self.sitename + ".com/" + self.identifier




INSTAGRAM = "instagram"

class InstagramAccount(Account):

    def __init__(self, username):
        super().__init__(username, INSTAGRAM)
        self.username = username
        self.parsed_homepage = self._retreive_parsed_profile_page()
        self.profile = InstagramProfileInfo(self._get_profile_json())
        self.posts = self._parse_posts()


    def _browser_cookies(self):
        return browser_cookie3.chrome(domain_name='.instagram.com')


    def _parse_posts(self):
        profile = self._get_profile_json()

        posts_metadata = profile['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']

        posts_json_list = posts_metadata['edges']
        
        posts = []

        for post_json in posts_json_list:
            post = InstagramPost(post_json)
            posts.append(post)

        return posts


    def get_recent_posts(self, count = 10):
        return self.posts


    def get_most_liked_post(self):
        most_liked = self.posts[0]
        for post in self.posts:
            if post.likes > most_liked.likes:
                most_liked = post
        return most_liked


    def get_most_commented_post(self):
        most_commented = self.posts[0]
        for post in self.posts:
            if post.comments > most_commented.comments:
                most_commented = post
        return most_commented


    def get_most_engaged_content(self):
        posts = self.get_recent_posts()  # [ InstagramPost... ]
        most_engaged_posts = self.posts  # grabbing all posts right now - for RK to edit 
        first_post = most_engaged_posts[0]
        first_post.comments

        most_engaged_post = first_post

        print(first_post.comments)
        # For Ricky to fill in:
        # Get the most engaged upon content

        # third_post = posts[2]

        # third_post.likes
        # third_post.comments

        print(most_engaged_post)

        return most_engaged_post


    def _get_profile_json(self):
        body = self.parsed_homepage.find('body').findAll('script', type="text/javascript")[0]

        json_raw = str(body).split("window._sharedData = ")[1].replace(';</script>','')
        
        json_parsed = json.loads(json_raw)

        return json_parsed


    def _parse_number_of_followers(self):
        profile = self._get_profile_json()

        number_of_followers = profile['entry_data']['ProfilePage'][0]['graphql']['user']["edge_followed_by"]["count"]

        return number_of_followers


class InstagramProfileInfo:
    def __init__(self, profile_json):
        user = profile_json['entry_data']['ProfilePage'][0]['graphql']['user']

        self.followers = user["edge_followed_by"]["count"]
        self.following = user["edge_follow"]["count"]
        self.profile_pic = user["profile_pic_url"]
        self.username = user["username"]
        self.identifier = user["id"]
        self.is_private = user["is_private"]

    def toString(self):
        string = (
            "Id: " + str(self.identifier) + "\n"
            "Username: " + str(self.username) + "\n"
            "Profile Pic: " + str(self.profile_pic) + "\n"
            "Followers: " + str(self.followers) + "\n"
            "Following: " + str(self.following) + "\n"
            "Is Private: " + str(self.is_private) + "\n"
        )
        return string




class InstagramPost:
    def __init__(self, post_json):
        self.post_json = post_json
        self.asset = InstagramContent.create(post_json)
        self._parsePostJson(post_json)


    def _parsePostJson(self, post_json):
        node = post_json['node']
        self.type = node['__typename']
        self.identifier = node['id']
        self.url = node['display_url']
        self.comments = node['edge_media_to_comment']['count']
        self.likes = node['edge_liked_by']['count']
        self.post_time = node['taken_at_timestamp']
        self.caption = node['edge_media_to_caption']['edges'][0]['node']['text']


    def toString(self):
        string = (
            "Id: " + str(self.identifier) + "\n"
            "Media Type: " + str(self.type) + "\n"
            "Caption: " + str(self.caption) + "\n"
            "Url: " + str(self.url) + "\n"
            "Post Time: " + str(self.post_time) + "\n"
            "Comments: " + str(self.comments) + "\n"
            "Likes: " + str(self.likes) + "\n"
        )
        return string



if __name__ == "__main__":
    account = InstagramAccount("koberdoodle")

    account2 = InstagramAccount("oregonfootball")

    print(account.profile.toString())

    print(account.get_most_commented_post().toString())

    account.get_most_engaged_content()