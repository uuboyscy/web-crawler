"""
Request the PTT movie page and extract its title.
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/movie/index.html"
res = requests.get(url)
soup = BeautifulSoup(
    res.text,
    "html.parser",
)
title = soup.title.text
print(title)  # This should print "看板 movie 文章列表 - 批踢踢實業坊"
