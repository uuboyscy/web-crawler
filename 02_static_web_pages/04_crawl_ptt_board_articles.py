"""Fetch PTT board article links and extract article text without metadata or comments."""

import re
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
    """Return article titles and URLs from the last board page visited.

    Args:
        board: PTT board name, such as ``photo``.
        page: Positive number of index pages to visit, starting with the latest
            and following the previous-page link toward older articles.

    Returns:
        Dictionaries with ``article_title`` and ``article_url`` keys from the
        final page visited. Stops early if no previous-page link exists.
    """

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
    """Fetch an article and return its main text with existing whitespace.

    Args:
        article_url: URL of a PTT article containing a ``#main-content`` element.

    Returns:
        Article text after removing metadata, reader comments, and PTT footer
        notices.
    """

    article_res = requests.get(article_url, headers=headers, timeout=10)
    article_soup = BeautifulSoup(article_res.text, "html.parser")
    main_contain_tag = article_soup.select_one("#main-content")

    # Remove article metadata, reader comments, and PTT footer notices.
    unused_tags = ".article-metaline, .article-metaline-right, .push, .f2"
    for unused_tag in main_contain_tag.select(unused_tags):
        unused_tag.extract()

    return main_contain_tag.text

def trans_title_to_valid_file_name(article_title: str) -> str:
    """Convert a PTT title to a safe filename stem, handling invalid names and length."""
    # Replace invalid filename characters and ASCII control characters with underscores.
    file_name = re.sub(r'[<>:"/\\|?*\x00-\x1f\x7f]', "_", article_title)
    # Keep up to 200 UTF-8 bytes and discard any incomplete character at the end.
    file_name = file_name.encode("utf-8")[:200].decode("utf-8", errors="ignore")
    # Trim whitespace and trailing dots; use "untitled" if the result is empty.
    file_name = file_name.strip().rstrip(". ") or "untitled"
    # Get the part before the first dot in uppercase for a case-insensitive check.
    reserved_name = file_name.split(".", 1)[0].upper()
    # Check Windows reserved device names.
    if reserved_name in {"CON", "PRN", "AUX", "NUL"} or re.fullmatch(
        # Match COM or LPT followed by a reserved digit, including superscripts.
        r"(?:COM|LPT)[1-9¹²³]", reserved_name
    ):
        # Prefix reserved names with an underscore so they can be used as filenames.
        file_name = f"_{file_name}"
    # Return the cleaned name; the caller adds the article ID and extension.
    return file_name

def run_crawler(board: str, page: int) -> None:
    """Save articles from the requested board page as UTF-8 text files."""

    output_path = Path("outputs") / Path(board)
    output_path.mkdir(parents=True, exist_ok=True)

    title_url_list = get_title_url_list(board, page)

    for title_url in title_url_list:
        article_title = title_url["article_title"]
        article_url = title_url["article_url"]
        article_content = extract_article(article_url)
        file_name = trans_title_to_valid_file_name(article_title)
        article_id = Path(article_url).stem
        article_path = output_path / f"{file_name}_{article_id}.txt"
        article_path.write_text(article_content, encoding="utf-8")


if __name__ == "__main__":
    board = "photo"
    page = 3

    run_crawler(board, page)
