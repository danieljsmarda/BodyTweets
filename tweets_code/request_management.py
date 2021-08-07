import time
import requests
import json
import shelve

settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    bearer_token = settings['bearer_token']
    cookie = settings['cookie']

payload={}
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': cookie
}

def handle_rate(request_fn):
    def wrapper(*args, max_time=900, **kwargs):
        start = time.time()
        request_fn(*args, **kwargs)
        end = time.time()
        elapsed = start - end
        if elapsed < max_time:
            time.sleep(max_time - elapsed + 1)
    return wrapper

def send_n_requests(raw_tweets_dump_path, batch_path, base_url, next_token='', n=5):
    '''n = Total number of requests to send in each 15-minute period'''
    with open(raw_tweets_dump_path, 'a', encoding='utf-16') as d, open(batch_path, 'a', encoding='utf-16') as b:
        b.truncate(0)
        url = base_url
        for i in range(n): # use 180 for maximum
            if next_token != '':
                url = base_url + f'&next_token={next_token}'
            response = requests.request('GET', url, headers=headers, data=payload)
            next_token = eval(response.text)['meta']['next_token']

            d.write('%s\n' % json.dumps(response.text))
            b.write('%s\n' % json.dumps(response.text))

            # 3 Second sleep = 300 requests / 15 minutes
            time.sleep(1.01)