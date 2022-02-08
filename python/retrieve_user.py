import requests
import browser_cookie3

cookies = browser_cookie3.chrome(domain_name='.instagram.com')

headers = {
	"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Accept-Encoding":"gzip, deflate", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
}

response = requests.get('https://www.instagram.com/mindmatterswithdiv/', verify=False, headers=headers, cookies=cookies, timeout=3)

print(response.text)