import requests
import browser_cookie3

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



if __name__ == "__main__":
    retriever = HTMLRetriever()
    response = retriever.retrieve("https://www.instagram.com/selfcare4yu/")

    print(str(response))