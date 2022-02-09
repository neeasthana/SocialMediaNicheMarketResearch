import requests
import browser_cookie3
from bs4 import BeautifulSoup

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

    def _browser_cookies(self):
        return browser_cookie3.chrome(domain_name='.instagram.com')

    def get_recent_posts(self):
        print (self.parsed_homepage.prettify())

account = InstagramAcccount("mindmatterswithdiv")
account.get_recent_posts()