import json
import pandas as pd
from tqdm import tqdm

settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    raw_tweets_batch_path = settings['filepaths']['raw_tweets_batch_path']
    batch_users_path = settings['filepaths']['batch_users_path']
    batch_tweets_path = settings['filepaths']['batch_tweets_path']


def handle_surrogates(text):
    return text.encode('utf-16', 'surrogatepass').decode('utf-16')

def handle_identifiers(line):
    # A bit of a hacky fix, but this handles leading BOM bytes in some tweets
    i = 0
    while True:
        try:
            return eval(eval(line[i:]))
        except SyntaxError: # unexpected char in identifier
            i += 1

def count_lines(filepath):
    '''Only used to calculate max results for progress bar.'''
    with open(filepath, 'r', encoding='utf-16-le') as f:
        return len(f.readlines())

def parse_raw_tweets(raw_tweets_path):
    '''While raw_tweets_path is a variable, the intention is to use this 
    with the raw_tweets_batch_path file.'''
    with open(raw_tweets_path, 'r', encoding='utf-16-le') as f:
        tweets_df = pd.DataFrame(columns=['author_id', 'tweet_id', 'tweet_text', 'created_at', 'next_token'])
        users_df = pd.DataFrame(columns=['author_id', 'location'])
        for line in tqdm(f, desc='Processing lines in batch file: ', total=count_lines(raw_tweets_path)):
            response = handle_identifiers(line)
            next_token = response['meta']['next_token']
            for tweet in response['data']:
                tweets_df = tweets_df.append({
                    'author_id': tweet['author_id'],
                    'tweet_id': tweet['id'],
                    # Handle surrogate pairs
                    'tweet_text': handle_surrogates(tweet['text']),
                    'created_at': tweet['created_at'],
                    'next_token': next_token
                }, ignore_index=True)
            for user in response['includes']['users']:
                try:
                    users_df = users_df.append({
                        'author_id': user['id'],
                        'location': handle_surrogates(user['location'])
                    }, ignore_index=True)
                except KeyError: # user doesn't have location string
                    continue

    tweets_df.to_parquet(batch_tweets_path, compression=None)
    users_df.to_parquet(batch_users_path, compression=None)