from retriever import HTMLRetriever, CachedHTMLRetriever
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
        self.followers = self._parse_number_of_followers()
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


    def get_most_engaged_content(self, count = 3):
        posts = self.get_recent_posts()  # [ InstagramPost... ]
        most_engaged_post = None

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



class InstagramPost:
    def __init__(self, post_json):
        self.post_json = post_json
        self._parsePostJson(post_json)


    def _parsePostJson(self, post_json):
        node = post_json['node']
        self.type = node['__typename']
        self.identifier = node['id']
        self.url = node['display_url']
        self.comments = node['edge_media_to_comment']['count']
        self.likes = node['edge_liked_by']['count']
        self.post_time = node['taken_at_timestamp']


    def toString(self):
        string = (
            "Id: " + str(self.identifier) + "\n"
            "Media Type: " + str(self.type) + "\n"
            "Url: " + str(self.url) + "\n"
            "Post Time: " + str(self.post_time) + "\n"
            "Comments: " + str(self.comments) + "\n"
            "Likes: " + str(self.likes) + "\n"
        )
        return string


if __name__ == "__main__":
    account = InstagramAccount("koberdoodle")

    print(account.followers)

    account.get_most_engaged_content()