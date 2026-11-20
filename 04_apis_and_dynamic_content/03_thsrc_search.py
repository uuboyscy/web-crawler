"""
Query the THSR timetable via its hidden POST API found in DevTools Network tab.
https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c
"""

from datetime import date

import requests

url = "https://www.thsrc.com.tw/TimeTable/Search"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36",
}

today = date.today().strftime("%Y/%m/%d")
search_time = "19:30"

data = {
    "SearchType": "S",
    "Lang": "TW",
    "StartStation": "NanGang",
    "EndStation": "ZuoYing",
    "OutWardSearchDate": today,
    "OutWardSearchTime": search_time,
    "ReturnSearchDate": today,
    "ReturnSearchTime": search_time,
    "DiscountType": "",
}

response = requests.post(url, headers=headers, data=data, timeout=10)
table = response.json()["data"]["DepartureTable"]
title = table["Title"]

print(f"{title['StartStationName']} -> {title['EndStationName']} ({title['TitleSplit1']})")
print("-" * 60)

# The API returns all trains for the day; filter for trains at or after search_time.
trains = [t for t in table["TrainItem"] if t["DepartureTime"] >= search_time]
for train in trains[:5]:
    stops = [s["StationName"] for s in train["StationInfo"] if s["Show"]]
    print(
        f"車次 {train['TrainNumber']} | "
        f"{train['DepartureTime']} -> {train['DestinationTime']} "
        f"({train['Duration']}) | "
        f"自由座: {train['NonReservedCar']}"
    )
    print(f"  停靠站: {' -> '.join(stops)}")
