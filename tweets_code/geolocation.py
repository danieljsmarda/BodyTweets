import shelve
import json
import pandas as pd
import numpy as np
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams
from read_tweets import parse_raw_tweets

settings_path = '../settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)
    batch_path = settings['filepaths']['batch_path']
    geolocation_users_path = settings['filepaths']['geolocation_users_path']
    geolocation_tweets_path = settings['filepaths']['geolocation_tweets_path']
    location_shelf_path = settings['filepaths']['location_shelf_path']
    interim_path = settings['filepaths']['interim_path']
    master_path = settings['filepaths']['master_path']


# Tweet Data
parse_raw_tweets(batch_path)
users_df = pd.read_parquet(geolocation_users_path)
tweets_df = pd.read_parquet(geolocation_tweets_path)
# Location Data loading
location_shelf = shelve.open(location_shelf_path)
state_strings = location_shelf['state_strings']
states_df = location_shelf['states_df']
states_dict = location_shelf['states_dict']
all_entities = location_shelf['all_entities']
location_shelf.close()


# --- String Processing functions ---
def get_ngrams(text, n):
    n_grams = ngrams(TweetTokenizer().tokenize(text), n)
    return [' '.join(grams) for grams in n_grams]
def get_state_from_loc_str(loc_s):
    tokens = get_ngrams(loc_s, 1) + get_ngrams(loc_s, 2)
    states = [states_dict[token] for token in tokens if token in state_strings]
    if 'District of Columbia' in states:
        return ['District of Columbia']
    else:
        return states

def city_search(loc_s):
    subset = all_entities[all_entities['name'].apply(lambda name: name in loc_s)]
    best_guess = subset.sort_values('pop', ascending=False).drop_duplicates(subset='name', keep='first')
    if best_guess.empty:
        return 'no match'
    state = best_guess.iloc[0,:]['state']
    if state is not None:
        return state
    elif best_guess.iloc[0,:]['is_foreign']:
        return 'foreign'

# --- Saving helper function ---
def append_results_parquet(file_location, data):
    file_name = file_location+'.parquet.gzip'
    try:
        df = pd.read_parquet(file_name)
    except FileNotFoundError as e:
        df = pd.DataFrame(columns=data.columns)
    finally:
        df = df.append(data)
        df.to_parquet(file_name, compression='gzip')


# -- Main function ---
def geolocate_tweets():
    merged = pd.merge(tweets_df, users_df, on='author_id')
    merged['state_from_loc_str'] = merged['location'].apply(get_state_from_loc_str)
    merged['state_from_city'] = merged['location'].apply(city_search)
    merged = merged.explode('state_from_loc_str')
    # Return state if state extracted straight from string,
    # city search otherwise.
    # This means that state matching takes precedence over foreign city matching.
    # Multiple US state matches are assigned one value to each matched state.
    # For duplicate matching on US city and foreign city, use highest population as estime.
    merged['final_state'] = np.where(~(merged['state_from_loc_str'].isna()), merged['state_from_loc_str'], merged['state_from_city'])
    # Only keep US data
    filtered = merged[~(merged['final_state'].isin(['no match', 'foreign']))]
    append_results_parquet(interim_path, filtered)
    append_results_parquet(master_path, filtered[['author_id', 'tweet_id', 'tweet_text', 'final_state']])