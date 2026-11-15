"""
Navigate from PTT's boards page to Gossiping and pass the over-18 prompt using a session.
Use this example only if you are eligible to access the board.
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}
boards_url = "https://www.ptt.cc/bbs/index.html"
over18_url = "https://www.ptt.cc/ask/over18"

with requests.Session() as session:
    session.headers.update(headers)

    # 1. Open the PTT boards page and find the path to the Gossiping board.
    boards_res = session.get(boards_url, timeout=10)
    boards_soup = BeautifulSoup(boards_res.text, "html.parser")

    gossiping_board = boards_soup.find("div", class_="board-name", string="Gossiping")
    gossiping_path = gossiping_board.find_parent("a")["href"]
    print("Gossiping board path:", gossiping_path)

    # 2. Open the age-confirmation page that browsers are sent to when over18=1 is missing.
    # (PTT's board page uses client-side JavaScript to redirect browsers to /ask/over18?from=...)
    over18_res = session.get(over18_url, params={"from": gossiping_path}, timeout=10)
    over18_soup = BeautifulSoup(over18_res.text, "html.parser")
    print("Age check URL:", over18_res.url)

    # 3. Extract the age-confirmation form and "click" the over-18 button ("yes").
    form = over18_soup.select_one('form[action="/ask/over18"]')
    post_url = urljoin(over18_res.url, form["action"])
    from_path = form.select_one('input[name="from"]')["value"]
    yes_button = form.select_one('button[name="yes"]')
    form_data = {
        "from": from_path,
        yes_button["name"]: yes_button["value"],
    }

    # Submitting the form receives Set-Cookie: over18=1 and 302-redirects to the board.
    board_res = session.post(post_url, data=form_data, timeout=10)
    print("Session cookies after submitting:", session.cookies.get_dict())
    print("Final board URL:", board_res.url)

    # 4. Parse and print article titles from the Gossiping board page.
    board_soup = BeautifulSoup(board_res.text, "html.parser")
    for link in board_soup.select("div.title a"):
        print(link.get_text(strip=True))
