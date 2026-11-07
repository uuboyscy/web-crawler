"""
Fetch and print article titles from PTT's Gossiping board using a cookie.

The ``over18=1`` cookie records age confirmation; it is not a login credential.
Use this example only if you are eligible to access the board.
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}
url = "https://www.ptt.cc/bbs/Gossiping/index.html"
# The over18=1 cookie tells PTT that age confirmation has been completed.
cookies = {"over18": "1"}

response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

for link in soup.select("div.title a"):
    print(link.get_text(strip=True))
