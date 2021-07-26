import requests
import json
import time

settings_file = json.load(open('tweets/settings.json'))
# Replace your bearer token below
bearer_token = settings_file['bearer_token']
cookie = settings_file['cookie']
max_results = 10
start_time = '2020-06-11T16:05:06.000Z'
end_time = '2020-06-11T16:20:00.000Z'
query = 'trump'

base_url = f'https://api.twitter.com/2/tweets/search/all?query={query}&start_time={start_time}&end_time={end_time}&max_results={max_results}'

payload={}
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': cookie
}


with open('tweets/downloaded_tweets.txt', 'w', encoding='utf-16') as f:
    next_url = base_url
    for i in range(15):
        response = requests.request('GET', next_url, headers=headers, data=payload)
        next_token = eval(response.text)['meta']['next_token']
        next_url = base_url + f'&next_token={next_token}'

        # Next step:
        f.write('%s\n' % json.dumps(response.text))

        # 3 Second sleep = 300 requests / 15 minutes
        time.sleep(1.01)