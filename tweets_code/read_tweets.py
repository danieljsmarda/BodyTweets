import json
import pandas as pd

settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    raw_tweets_batch_path = settings['filepaths']['raw_tweets_batch_path']
    batch_users_path = settings['filepaths']['batch_users_path']
    batch_tweets_path = settings['filepaths']['batch_tweets_path']


def handle_surrogates(text):
    return text.encode('utf-16', 'surrogatepass').decode('utf-16')

def parse_raw_tweets(raw_tweets_batch_path):
    with open(raw_tweets_batch_path, 'r', encoding='utf-16-le') as f:
        response = eval(eval(f.readline()))
        tweets_df = pd.DataFrame(columns=['author_id', 'tweet_id', 'tweet_text', 'created_at'])
        users_df = pd.DataFrame(columns=['author_id', 'location'])
        for tweet in response['data']:
            # Handle surrogate pairs
            tweets_df = tweets_df.append({
                'author_id': tweet['author_id'],
                'tweet_id': tweet['id'],
                'tweet_text': handle_surrogates(tweet['text']),
                'created_at': tweet['created_at']
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