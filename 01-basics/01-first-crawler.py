"""
Request the PTT photo page and extract its title.
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/photo/index.html"
res = requests.get(url)
soup = BeautifulSoup(
    res.text,
    "html.parser",
)
title = soup.title.text
print(title)  # This should print "看板 photo 文章列表 - 批踢踢實業坊"
