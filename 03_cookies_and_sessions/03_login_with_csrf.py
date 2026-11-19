"""Log in to Quotes to Scrape by extracting a hidden CSRF token with a session."""

import requests
from bs4 import BeautifulSoup

login_url = "https://quotes.toscrape.com/login"

with requests.Session() as session:
    # 1. GET the login page to receive the initial session cookie and hidden CSRF token.
    login_page_res = session.get(login_url, timeout=10)
    login_page_soup = BeautifulSoup(login_page_res.text, "html.parser")

    csrf_token = login_page_soup.select_one('input[name="csrf_token"]')["value"]
    print("CSRF token:", csrf_token)
    print("Cookies before login:", session.cookies.get_dict())

    # 2. Compose form data with the CSRF token, username, and password.
    # (quotes.toscrape.com is a practice site that accepts any username/password.)
    form_data = {
        "csrf_token": csrf_token,
        "username": "demo_user",
        "password": "demo_password",
    }

    # 3. POST the form data; the session sends the cookie from Step 1 automatically.
    home_res = session.post(login_url, data=form_data, timeout=10)
    print("Cookies after login:", session.cookies.get_dict())

    # 4. Verify login succeeded by checking for the Logout link on the page.
    home_soup = BeautifulSoup(home_res.text, "html.parser")
    logout_link = home_soup.select_one('a[href="/logout"]')
    print("Logged in:", logout_link is not None)
