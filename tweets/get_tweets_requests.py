import requests
import json

settings_file = json.load(open("settings.json"))
# Replace your bearer token below
bearer_token=settings_file["bearer_token"]

url = "https://api.twitter.com/2/tweets/search/all?query=trump&start_time=2020-06-11T16:05:06.000Z&end_time=2020-06-11T16:20:06.000Z&max_results=10"

payload={}
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': 'guest_id=v1%3A162634498705730258; personalization_id="v1_CpW3pGCqGu0WcG2AdkGNGw=="'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
