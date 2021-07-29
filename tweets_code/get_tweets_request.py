import requests
import json
import time

settings_path = '../settings.json'
write_path = '../private_data/downloaded_tweets.txt'

with open(settings_path, 'r') as f:
    settings_file = json.load(f)
    bearer_token = settings_file['bearer_token']
    cookie = settings_file['cookie']

# Replace your bearer token below
params = {
    'max_results' : '10',
    'start_time' : '2020-06-11T16:05:06.000Z',
    'end_time' : '2020-06-11T16:20:00.000Z',
    'query' : 'trump lang:en',
    'tweet.fields' : 'author_id',
    'expansions' : 'author_id',
    'user.fields' : 'location'
}

base_url = 'https://api.twitter.com/2/tweets/search/all'

payload=params
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': cookie
}


with open(write_path, 'w', encoding='utf-16') as f:
    for i in range(5):
        response = requests.get(base_url, headers=headers, params=payload)
        next_token = eval(response.text)['meta']['next_token']
        payload['next_token'] = next_token

        # Next step:
        f.write('%s\n' % json.dumps(response.text))

        # 3 Second sleep = 300 requests / 15 minutes
        time.sleep(1.01)