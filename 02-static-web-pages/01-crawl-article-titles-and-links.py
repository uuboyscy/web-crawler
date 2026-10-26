"""Print article titles and links from five pages of the PTT photo board."""

import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/photo/index.html"
page_count = 5

for page in range(1, page_count + 1):
    print(f"\n========== Page {page} ==========")
    print(url)

    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    # Select article links; deleted articles without links are skipped.
    links = soup.select(".title a")
    for link in links:
        print(link.get_text(strip=True))
        # PTT uses relative links. Convert them into complete URLs.
        print(urljoin(url, link["href"]))

    if page == page_count:
        break

    # Find the previous board page by its label instead of guessing its number.
    previous_page = soup.find("a", string="‹ 上頁")
    if previous_page is None:
        print("No previous page found.")
        break

    url = urljoin(url, previous_page["href"])
    time.sleep(1)  # Pause between pages to avoid sending requests too quickly.
