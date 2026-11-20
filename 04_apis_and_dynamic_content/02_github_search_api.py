"""
Search GitHub repositories using GET query parameters and pagination.
API docs: https://docs.github.com/en/rest/search/search#search-repositories
"""

import requests

url = "https://api.github.com/search/repositories"
headers = {
    "Accept": "application/vnd.github+json",
}

for page in range(1, 3):
    params = {
        "q": "data engineering language:python",
        "sort": "stars",
        "order": "desc",
        "per_page": 5,
        "page": page,
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()

    print(f"=== Page {page} (Total matches: {data['total_count']}) ===")
    print("Request URL:", response.url)

    for repo in data["items"]:
        print(f"- {repo['full_name']} ({repo['stargazers_count']} stars)")
        print(f"  {repo['html_url']}")
    print()
