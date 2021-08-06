from request_management import send_n_requests
from geolocation import geolocate_tweets

dump_path = '../private_data/dump.txt'
batch_path = '../private_data/batch.txt'

params = {
    'max_results' : '500', # Results per request
    'start_time' : '2020-06-11T16:05:06.000Z',
    'end_time' : '2020-06-11T16:20:00.000Z',
    'query' : 'trump lang:en',
    'tweet.fields' : 'author_id',
    'expansions' : 'author_id',
    'user.fields' : 'location'
}
params_string = '&'.join([key + '=' + value for key, value in params.items()])
base_url = 'https://api.twitter.com/2/tweets/search/all?' + params_string

def extract_next_token(filename):
    with open(filename, 'r', encoding='utf-16-le') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        next_token = eval(eval(last_line))['meta']['next_token']
    return next_token

def init_batch():
    for i in range(1):
        next_token = extract_next_token(batch_path)
        send_n_requests(dump_path, batch_path, base_url, next_token=next_token, n=1)
        geolocate_tweets()
init_batch()