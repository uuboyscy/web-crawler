import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}

template_board_url = "https://www.ptt.cc/bbs/{}/index.html"

def get_title_url_list(board: str, page: int = 1) -> list[dict[str, str]]:

    url = template_board_url.format(board)

    for _ in range(page):
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title_url_list = []
        links = soup.select(".title a")
        for link in links:
            article_title = link.get_text(strip=True)
            article_url = urljoin(url, link["href"])
            title_url_list.append(
                {
                    "article_title": article_title,
                    "article_url": article_url,
                }
            )

        previous_page = soup.find("a", string="‹ 上頁")
        if previous_page is None:
            print("No previous page found.")
            break

        url = urljoin(url, previous_page["href"])
        time.sleep(1)

    return title_url_list

def extract_article(article_url: str) -> str:

    article_res = requests.get(article_url, headers=headers, timeout=10)
    article_soup = BeautifulSoup(article_res.text, "html.parser")
    main_contain_tag = article_soup.select_one("#main-content")

    # Remove article metadata, reader comments, and PTT footer notices.
    unused_tags = ".article-metaline, .article-metaline-right, .push, .f2"
    for unused_tag in main_contain_tag.select(unused_tags):
        unused_tag.extract()

    return main_contain_tag.text


if __name__ == "__main__":
    board = "photo"
    page = 3

    title_url_list = get_title_url_list(board, page)

    for title_url in title_url_list:
        article_title = title_url.get("article_title")
        article_url = title_url.get("article_url")
        article_content = extract_article(article_url)
        print(article_title)
        print(article_url)
        print(article_content)
        print()
