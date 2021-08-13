import json
import logging
import time
import os
from itertools import cycle
from request_management import send_n_requests
from file_utils import handle_identifiers


# -------------------- Load paths and raw data -----------------------
# Start run
run_time = time.ctime()

# Load filepaths from settings
settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    raw_tweets_runs_dir = settings['filepaths']['raw_tweets_runs_dir']
    current_run_dir = os.path.join(raw_tweets_runs_dir, run_time) + '/'
    os.mkdir(current_run_dir)
    raw_tweets_dump_path = current_run_dir + 'dump.txt'
    raw_tweets_batch_path = current_run_dir + 'batch.txt'
    batch_users_path = settings['filepaths']['batch_users_path']
    batch_tweets_path = settings['filepaths']['batch_tweets_path']
    query_times_path = settings['filepaths']['query_times_path']

#log_path = raw_tweets_runs_dir + run_time + '.log'
logging.basicConfig(level=logging.INFO, filename=current_run_dir + 'logfile.log')


# Define query inputs
with open('../public_data/body_vocab.txt', 'r') as f:
    body_words_list = [word.strip() for word in f.readlines()]
body_words_string = '(' + ' OR '.join(body_words_list) + ')'

start_times = cycle([
    '2013-01-01T00:00:00.000Z',
    '2015-11-01T00:00:00.000Z',
    '2017-05-01T00:00:00.000Z',
    '2019-09-15T00:00:00.000Z',
    '2021-02-01T00:00:00.000Z',
])

logging.info('These were taken two days earlier than initial plan.')
'''
end_times = cycle([
    '2013-01-28T19:00:00.000Z',
    '2015-12-06T12:00:00.000Z',
    '2017-06-02T02:00:00.000Z',
    '2019-10-16T02:00:00.000Z',
    '2021-03-01T12:00:00.000Z'
])
'''
end_times = cycle([
    '2013-01-26T19:00:00.000Z',
    '2015-12-04T12:00:00.000Z',
    '2017-05-31T02:00:00.000Z',
    '2019-10-14T02:00:00.000Z',
    '2021-02-27T12:00:00.000Z'
])
logging.info(f'The end_times for this run are {str(end_times)}')

MAX_RESULTS = 500

# -------------------- Query Processing Functions -----------------------
def get_url(start_time, end_time):
    params = {
        'max_results' : str(MAX_RESULTS), # Results per request
        'start_time' : start_time,
        'end_time' : end_time,
        'query' : body_words_string + ' (lang:en OR lang:und) -is:nullcast',
        #'tweet.fields' : 'author_id,created_at',
        'tweet.fields': 'author_id,created_at,lang,public_metrics',
        'expansions' : 'author_id',
        'user.fields' : 'location'
    }
    # To keep track of queries
    with open(query_times_path, 'w') as f:
        f.write(params['start_time']); f.write(params['end_time'])

    params_string = '&'.join([key + '=' + value for key, value in params.items()])
    base_url = 'https://api.twitter.com/2/tweets/search/all?' + params_string
    return base_url

def extract_next_token(filename):
    with open(filename, 'r', encoding='utf-16-le') as f:
        lines = f.read().splitlines()
    try:
        last_line = lines[-1]
        next_token = eval(eval(last_line))['meta']['next_token']
    except IndexError: # list/file is empty
        next_token = ''
    except SyntaxError: # BOM Error:
        next_token = handle_identifiers(last_line)['meta']['next_token']
    return next_token

def add_year_to_path(txtfilepath, year):
    return txtfilepath[:-4] + '-' + year + '.txt'


# -------------------- Main  -----------------------
def init_batch(desired_tweets, n_requests=1):
    logging.info(f'Total requested tweets: {desired_tweets}.')
    collected_tweets = 0
    while collected_tweets < desired_tweets:
        start_time = next(start_times)
        end_time = next(end_times)
        year = start_time[:4]
        # Get next_token if exists
        try:
            next_token = extract_next_token(add_year_to_path(raw_tweets_batch_path, year))
        except FileNotFoundError: # previous file doesn't exist yet
            next_token = ''
        
        dump_path = add_year_to_path(raw_tweets_dump_path, year)
        batch_path = add_year_to_path(raw_tweets_batch_path, year)
        base_url = get_url(start_time, end_time)
        try:
            send_n_requests(dump_path, batch_path,
                base_url, next_token=next_token, n=n_requests)
            collected_tweets += MAX_RESULTS * n_requests
            logging.info(f'{MAX_RESULTS * n_requests} tweets saved to batch path {batch_path}')
            logging.info(f'Total number of tweets collected is now {collected_tweets}')
            print(f'Total number of tweets: {collected_tweets}')
        except Exception as e:
            logging.exception("Surprise Exception: ")
            time.sleep(120)
        

if __name__ == '__main__':
    init_batch(1000000, n_requests=1)