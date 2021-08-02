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

params_string = '&'.join([key + '=' + value for key, value in params.items()])
base_url = 'https://api.twitter.com/2/tweets/search/all?' + params_string

payload={}
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': cookie
}


def handle_rate(request_fn):
    def wrapper(max_time=900):
        start = time.time()
        request_fn()
        end = time.time()
        elapsed = start - end
        if elapsed < max_time:
            time.sleep(max_time - elapsed + 1)
    return wrapper

@handle_rate
def send_requests():
    with open(write_path, 'w', encoding='utf-16') as f:
        next_url = base_url
        for i in range(5): # use 180 for maximum
            response = requests.request('GET', next_url, headers=headers, data=payload)
            next_token = eval(response.text)['meta']['next_token']
            next_url = base_url + f'&next_token={next_token}'

            # Next step:
            f.write('%s\n' % json.dumps(response.text))

            # 3 Second sleep = 300 requests / 15 minutes
            time.sleep(1.01)
            
send_requests(max_time=10)