"""Send simple GET and POST requests and inspect HTTPBin's responses."""

import requests

# User-Agent: send a browser-style client identification string.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}

# GET: params= adds query parameters to the URL.
# timeout limits how long Requests waits for a connection or response data.
url = "https://httpbin.org/get"
params = {"topic": "web crawling"}
res = requests.get(url, params=params, headers=headers, timeout=10)
print("GET status:", res.status_code)  # 200 means OK.
# The JSON response includes query parameters (args) and received headers.
print(res.text)  # .text returns the response body as a string.

print()
print("================================")
print()

# POST: HTTPBin echoes the submitted data without creating a real post.
data = {"topic": "web crawling"}
# data= sends this dictionary as form fields.
res = requests.post("https://httpbin.org/post", data=data, headers=headers, timeout=10)
print("POST form result:")
print(res.text)  # Includes form fields (form) and received headers.

print()
print("================================")
print()

# Use json= instead of data= to send a JSON body.
res = requests.post("https://httpbin.org/post", json=data, headers=headers, timeout=10)
print("POST JSON result:")
print(res.text)  # Includes the JSON body (json) and received headers.
