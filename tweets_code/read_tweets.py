import pandas as pd
import shelve

def handle_surrogates(text):
    return text.encode('utf-16', 'surrogatepass').decode('utf-16')

tweet_processing_shelf_path = '../private_data/tweet_processing'

def parse_raw_tweets(batch_path):
    shelf = shelve.open(tweet_processing_shelf_path)
    with open(batch_path, 'r', encoding='utf-16-le') as f:
        response = eval(eval(f.readline()))
        tweets_df = pd.DataFrame(columns=['author_id', 'tweet_id', 'tweet_text'])
        users_df = pd.DataFrame(coumns=['author_id', 'location'])
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
        shelf['next_token'] = response['meta']['next_token']
        shelf['raw_tweets_df'] = tweets_df
        shelf['users_df'] = users_df
        shelf['
    shelf.close()
