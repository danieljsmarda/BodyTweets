import json
from send_requests import send_n_requests

dump_path = '../private_data/dump.txt'
batch_path = '../private_data/batch.txt'

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

for in range(3):
    send_n_requests(dump_path, batch_path, base_url, n=5, max_time=3)

