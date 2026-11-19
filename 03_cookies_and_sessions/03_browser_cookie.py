"""Crawl PTT's Gossiping board using cookies saved in Chrome."""

import browser_cookie3
import requests
from bs4 import BeautifulSoup


def _fetch_cookies_from_browser() -> dict[str, str]:
    """Return the ``over18`` cookie from Chrome for ``ptt.cc``."""
    # May prompt for macOS Keychain access to decrypt Chrome cookies.
    cookie_jar = browser_cookie3.chrome(domain_name="ptt.cc")
    local_cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)

    cookies = {
        "over18": local_cookie_dict.get("over18")
    }

    print("[Fetched Cookies]", cookies)
    return cookies


def crawl_ptt_gossiping() -> None:
    """Fetch and print article titles from PTT's Gossiping board."""
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    cookies = _fetch_cookies_from_browser()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        print(f"Failed to retrieve page, status: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.title a")

    print("\n🔥 Latest Posts on PTT Gossiping:")
    for article in articles:
        print(f"- {article.text.strip()} ({article['href']})")


if __name__ == "__main__":
    crawl_ptt_gossiping()
