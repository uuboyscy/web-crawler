"""
Print a PTT article's direct text nodes, excluding text inside child tags.

Use recursive=False to skip nested metadata, comments, and footer tags.
Text inside article links or other nested formatting is also skipped.
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}

article_url = "https://www.ptt.cc/bbs/photo/M.1789550271.A.3C7.html"

article_res = requests.get(article_url, headers=headers, timeout=10)
article_soup = BeautifulSoup(article_res.text, "html.parser")
main_contain_tag = article_soup.select_one("#main-content")

text_list = main_contain_tag.find_all(string=True, recursive=False)

print("".join(text_list))
