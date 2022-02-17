import requests
import browser_cookie3
import time
import os

class URLRetriever:
    def retrieve(self, url, cookies = None, headers = {}, timeout = 3):
        response = requests.get(url, verify=False, headers=headers, cookies=cookies, timeout=timeout)
        return response.text



BROWSER_HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding":"gzip, deflate", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
}

class HTMLRetriever(URLRetriever):
    def retrieve(self, url):
        browser_cookies = HTMLRetriever._browser_cookies()
        return super().retrieve(url, cookies = browser_cookies, headers = BROWSER_HEADERS)


    def _browser_cookies(domain = '.instagram.com'):
        return browser_cookie3.chrome(domain_name = domain)



class CachedHTMLRetriever(HTMLRetriever):
    SIXTY_SECONDS = 60
    SIXTY_MINUTES = 60
    TWENTY_FOUR_HOURS = 24
    ONE_DAY = TWENTY_FOUR_HOURS * SIXTY_MINUTES * SIXTY_SECONDS;

    def __init__(self, seconds_til_expiration = ONE_DAY):
        self.seconds_til_expiration = seconds_til_expiration
        self._create_cache_folder()
        self.last_accessed = self._get_last_access_map()
        self.html_cache = self._get_html_cache()


    def _create_cache_folder(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '.cache')
        if not os.path.exists(path):
            os.mkdir(path)


    def _get_last_access_map(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '.cache/last_accessed_map.txt')

        return {}


    def _get_html_cache(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '.cache/html_cache_map.txt')

        return {}


    def retrieve(self, url):
        if url in self.html_cache and self._is_not_expired(url):
            return self._get_html_cache[url]
        else:
            response = super().retrieve(url)
            self._add_to_cache(url, response)
            return response


    def _add_to_cache(self, url, response):
        self.html_cache[url] = response
        self.last_accessed[url] = time.time()


    def _is_not_expired(self, url):
        now = time.time()
        then = self.last_accessed[url]
        difference = now - then
        return difference > self.seconds_til_expiration



if __name__ == "__main__":
    retriever = CachedHTMLRetriever()
    response = retriever.retrieve("https://www.instagram.com/selfcare4yu/")

    print(str(response))