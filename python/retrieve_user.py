import requests
import browser_cookie3
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


class Account:
    def __init__(self, identifier, sitename):
        self.identifier = identifier
        self.sitename = sitename


    def _retreive_parsed_profile_page(self):
        response = self._retreive_profile_page()
        return BeautifulSoup(response.text, 'html.parser')


    def _retreive_profile_page(self):
        url = self._generate_account_url()
        cookies = self._browser_cookies()
        response = requests.get(url, verify=False, headers=HEADERS, cookies=cookies, timeout=3)

        return response


    def _generate_account_url(self):
        return "https://www." + self.sitename + ".com/" + self.identifier




INSTAGRAM = "instagram"

class InstagramAcccount(Account):

    def __init__(self, username):
        super().__init__(username, INSTAGRAM)
        self.username = username
        self.parsed_homepage = self._retreive_parsed_profile_page()
        self.posts = self._parse_posts()


    def _browser_cookies(self):
        return browser_cookie3.chrome(domain_name='.instagram.com')


    def _parse_posts(self):
        profile = self._get_profile_json()

        posts_metadata = profile['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']

        posts_json_list = posts_metadata['edges']

        print("Count = " + str(posts_metadata['count']))
        
        posts = []

        for post_json in posts_json_list:
            post = InstagramPost(post_json)
            posts.append(post)

        return posts


    def get_recent_posts(self, count = 10):
        return self.posts


    def _get_profile_json(self):
        body = self.parsed_homepage.find('body').findAll('script', type="text/javascript")[0]

        json_raw = str(body).split("window._sharedData = ")[1].replace(';</script>','')
        
        json_parsed = json.loads(json_raw)

        return json_parsed



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


account = InstagramAcccount("cryptocasey")

for a in account.get_recent_posts():
    print(a.toString() + "\n\n")