import json
import pandas as pd

settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    batch_path = settings['filepaths']['batch_path']
    geolocation_users_path = settings['filepaths']['geolocation_users_path']
    geolocation_tweets_path = settings['filepaths']['geolocation_tweets_path']

#batch_path = '../private_data/batch.txt'
#geolocation_users_path = '../private_data/interim/geolocation_users.parquet'
#geolocation_tweets_path = '../private_data/interim/geolocation_tweets.parquet'

def handle_surrogates(text):
    return text.encode('utf-16', 'surrogatepass').decode('utf-16')

def parse_raw_tweets(batch_path):
    with open(batch_path, 'r', encoding='utf-16-le') as f:
        response = eval(eval(f.readline()))
        tweets_df = pd.DataFrame(columns=['author_id', 'tweet_id', 'tweet_text'])
        users_df = pd.DataFrame(columns=['author_id', 'location'])
        for tweet in response['data']:
            # Handle surrogate pairs
            tweets_df = tweets_df.append({
                'author_id': tweet['author_id'],
                'tweet_id': tweet['id'],
                'tweet_text': handle_surrogates(tweet['text'])
            }, ignore_index=True)
        for user in response['includes']['users']:
            try:
                users_df = users_df.append({
                    'author_id': user['id'],
                    'location': handle_surrogates(user['location'])
                }, ignore_index=True)
            except KeyError: # user doesn't have location string
                continue
        tweets_df.to_parquet(geolocation_tweets_path, compression=None)
        users_df.to_parquet(geolocation_users_path, compression=None)