import requests
import browser_cookie3
import time
import os
import pickle

class URLRetriever:
    def retrieve(self, url, cookies = None, headers = {}, timeout = 3, stream = false):
        response = requests.get(url, verify=False, headers=headers, cookies=cookies, timeout=timeout)
        return response


class ContentRetriever(URLRetriever):
    def retrieve(self, url):
        response = super().retrieve(url, cookies = None, stream = true)
        return response



class FileCachedRetriever(ContentRetriever):
    def __init__(self, cache_location = os.path.join(os.path.dirname(__file__), '.cache')):
        self.cache_location = cache_location
        self._create_cache_folder()


    def _create_cache_folder(self):
        path = self.cache_location
        if not os.path.exists(path):
            os.mkdir(path)


    def url_to_filename(url):
        return url.split("?")[0].replace("https://", "").split("/")[-1]


    def retrieve(self, url):
        filename = FileCachedRetriever.url_to_filename(url)
        path = os.path.join(self.cache_location, filename)
        file_exists = os.path.isfile(path)

        if not file_exists:
            with open(path, 'wb') as handle:
                response = super().retrieve(url)
                if not response.ok:
                    raise("Response was not a success: " + str(response))
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

        return filename



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
        return super().retrieve(url, cookies = browser_cookies, headers = BROWSER_HEADERS).text


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

        if not os.path.exists(path):
            with open(path, "wb") as f:
                pickle.dump({}, f)

        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except EOFError:
                return {}


    def _get_html_cache(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '.cache/html_cache_map.txt')

        if not os.path.exists(path):
            with open(path, "wb") as f:
                pickle.dump({}, f)

        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except EOFError:
                return {}


    def retrieve(self, url):
        if url in self.html_cache and self._is_not_expired(url):
            return self.html_cache[url]
        else:
            response = super().retrieve(url)
            self._add_to_cache(url, response)
            return response


    def _add_to_cache(self, url, response):
        self.html_cache[url] = response
        self.last_accessed[url] = time.time()
        self._refresh_cache()


    def _refresh_cache(self):
        dirname = os.path.dirname(__file__)
        last_accessed_path = os.path.join(dirname, '.cache/last_accessed_map.txt')
        html_cache_path = os.path.join(dirname, '.cache/html_cache_map.txt')

        with open(last_accessed_path, "wb") as f:
            pickle.dump(self.last_accessed, f)

        with open(html_cache_path, "wb") as f:
            pickle.dump(self.html_cache, f)


    def _is_not_expired(self, url):
        now = time.time()
        then = self.last_accessed[url]
        difference = now - then
        return difference < self.seconds_til_expiration



if __name__ == "__main__":
    retriever = CachedHTMLRetriever()
    response = retriever.retrieve("https://www.instagram.com/selfcare4yu/")

    print(response)