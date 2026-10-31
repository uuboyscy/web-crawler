"""
Print a PTT article's text after removing unwanted tags with extract().

Remove metadata, comments, and footer notices from #main-content, then use
.text to keep the remaining article text, including text inside nested tags.
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

# Remove article metadata, reader comments, and PTT footer notices.
unused_tags = ".article-metaline, .article-metaline-right, .push, .f2"
for unused_tag in main_contain_tag.select(unused_tags):
    unused_tag.extract()

# Unlike direct text nodes, .text also includes text inside links and formatting.
print(main_contain_tag.text)
