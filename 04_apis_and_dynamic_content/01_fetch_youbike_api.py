"""
Fetch live Taipei YouBike 2.0 station data from a public JSON API.
https://data.taipei/dataset/detail?id=c6bc8aed-557d-41d5-bfb1-8da24f78f2fb
"""

import requests

url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

response = requests.get(url, timeout=10)
# Parse the JSON response directly into Python lists and dicts (no BeautifulSoup needed).
stations = response.json()

print(f"Total stations: {len(stations)}\n")

# Print the first 5 stations as a quick preview.
for station in stations[:5]:
    print(f"Station: {station['sna']} ({station['sarea']})")
    print(f"  Available bikes: {station['available_rent_bikes']}")
    print(f"  Empty docks:     {station['available_return_bikes']}")
    print(f"  Updated at:      {station['mday']}")
