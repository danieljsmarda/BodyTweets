import requests
import json

settings_file = json.load(open('tweets/settings.json'))
# Replace your bearer token below
bearer_token = settings_file['bearer_token']
cookie = settings_file['cookie']
max_results = 10
start_time = '2020-06-11T16:05:06.000Z'
end_time = '2020-06-11T16:20:00.000Z'
query = 'trump'

url = f'https://api.twitter.com/2/tweets/search/all?query={query}&start_time={start_time}&end_time={end_time}&max_results={max_results}'

payload={}
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': cookie
}

response = requests.request('GET', url, headers=headers, data=payload)

print(response.text)
