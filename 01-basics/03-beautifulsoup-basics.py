"""Extract text and links with Beautiful Soup.

Usage:
    soup = BeautifulSoup(html, "html.parser")
    soup.select(".title a")                     # Find tags by CSS selector.
    soup.select_one(".title a")                 # Find the first matching tag.
    soup.find_all("div", attrs={"class": "title"})  # Find tags by attributes.
    soup.find("div", attrs={"class": "title"})  # Find the first matching tag.
    tag.get_text(strip=True)                   # Extract text, trimming whitespace.
    tag["href"]                                # Read an attribute.

select() and find_all(): list-like collections; empty when nothing matches.
select_one() and find(): the first matching Tag directly, or None if absent.
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}
url = "https://www.ptt.cc/bbs/movie/index.html"
res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

# Extract and clean the page title.
print("Extract and clean the page title.\n---")
print(soup.title.get_text(strip=True))

print()
print("==========")
print()

# select() uses CSS selectors: .title means class="title"; a means <a>.
# It returns a list-like collection, even with only one match.
print("Extract and print title information.")
print("select(\".title a\") returns a list of tag.")
print("---")
links = soup.select(".title a")
for link in links:
    print(link.get_text(strip=True))
    print(link["href"])  # Read the link's href attribute.

print()
print("==========")
print()

# select_one() returns one Tag directly, so no loop is needed.
print("Extract and print the first title and link.")
print('select_one(".title a") returns one Tag directly, or None if no match.')
print("---")
link = soup.select_one(".title a")
if link is not None:  # Check before using it: no match returns None.
    print(link.get_text(strip=True))
    print(link["href"])

print()
print("==========")
print()

# find_all() searches by tag name and attributes.
# Like select(), it returns a list-like collection, even for one match.
print("Extract and print title information.")
print('find_all("div", attrs={"class": "title"}) returns a list-like collection of tags.')
print("---")
title_divs = soup.find_all("div", attrs={"class": "title"})
for title_div in title_divs:
    # Search inside each div. Deleted articles may have no link.
    for link in title_div.find_all("a"):
        print(link.get_text(strip=True))

print()
print("==========")
print()

# find() returns the first matching Tag directly, or None.
print("Extract and print the first title container's text.")
print('find("div", attrs={"class": "title"}) returns one Tag directly, or None if no match.')
print("---")
title_div = soup.find("div", attrs={"class": "title"})
if title_div is not None:
    print(title_div.get_text(strip=True))
