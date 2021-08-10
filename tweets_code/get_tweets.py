import json
from request_management import send_n_requests
from geolocation import geolocate_tweets

settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    raw_tweets_dump_path = settings['filepaths']['raw_tweets_dump_path']
    raw_tweets_batch_path = settings['filepaths']['raw_tweets_batch_path']
    batch_users_path = settings['filepaths']['batch_users_path']
    batch_tweets_path = settings['filepaths']['batch_tweets_path']
    query_times_path = settings['filepaths']['query_times_path']

with open('../public_data/body_vocab.txt', 'r') as f:
    body_words_list = [word.strip() for word in f.readlines()]

body_words_string = '(' + ' OR '.join(body_words_list) + ')'

params = {
    'max_results' : '500', # Results per request
    'start_time' : '2019-10-01T05:00:00.000Z',
    'end_time' : '2019-10-15T16:59:00.000Z',
    'query' : body_words_string + ' (lang:en OR lang:und) -is:nullcast',
    'tweet.fields' : 'author_id,created_at',
    'expansions' : 'author_id',
    'user.fields' : 'location'
}
# To keep track of queries
with open(query_times_path, 'w') as f:
    f.write(params['start_time']); f.write(params['end_time'])

params_string = '&'.join([key + '=' + value for key, value in params.items()])
base_url = 'https://api.twitter.com/2/tweets/search/all?' + params_string

def extract_next_token(filename):
    with open(filename, 'r', encoding='utf-16-le') as f:
        lines = f.read().splitlines()
    try:
        last_line = lines[-1]
        next_token = eval(eval(last_line))['meta']['next_token']
    except IndexError: # list/file is empty
        next_token = ''
    return next_token

def init_batch():
    next_token = ''
    for i in range(1):
        send_n_requests(raw_tweets_dump_path, raw_tweets_batch_path, base_url, next_token=next_token, n=180)
        next_token = extract_next_token(raw_tweets_batch_path)
    geolocate_tweets()

if __name__ == '__main__':
    init_batch()