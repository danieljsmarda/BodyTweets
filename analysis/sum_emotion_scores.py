import json
import swifter
import pandas as pd
from tqdm import tqdm

# Create master df by concatenating all geolocated filepaths.

processed_files = [
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Tue Aug 10 19:52:42 2021/2013relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Tue Aug 10 19:52:42 2021/2015relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Tue Aug 10 19:52:42 2021/2017relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Tue Aug 10 19:52:42 2021/2019relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Tue Aug 10 19:52:42 2021/2021relevant_columns.parquet.gzip', # 5
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Wed Aug 11 12:52:17 2021/2013relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Wed Aug 11 12:52:17 2021/2015relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Wed Aug 11 12:52:17 2021/2017relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Wed Aug 11 12:52:17 2021/2019relevant_columns.parquet.gzip',
    '/dlabdata1/smarda/private_data/tweet_collection_runs/Wed Aug 11 12:52:17 2021/2021relevant_columns.parquet.gzip', # 5
]

df = pd.read_parquet(processed_files[0])
for filepath in processed_files:
    df = df.append(pd.read_parquet(filepath))
df = df.drop_duplicates(subset=['tweet_id', 'final_state'], keep='first')

# At this point, go to torchMoji-fork/examples/bodytweets_score_text_emojis.py

# Read in output of torchmoji and process
tm_raw_outputs_path = '/dlabdata1/smarda/private_data/master/torchmoji_raw_outputs.parquet.gzip'
tm_df = pd.read_parquet(tm_raw_outputs_path)
num_scores = 64
score_cols = [f'Rank_{i}_Score' for i in range(1, num_scores+1)]
with open('../public_data/emoji_mappings.json', 'r') as f:
    emoji_mappings = json.load(f)

for col_name in tqdm(score_cols, desc='Converting Types: '):
    tm_df[col_name] = pd.to_numeric(tm_df[col_name])

def extract_emotions(row, target_emotion):
    emotion_score = 0
    for rank in range(1, num_scores+1):
        emoji_idx = row[f'Rank_{rank}_Emoji']
        emotion = emoji_mappings[emoji_idx]
        if emotion == target_emotion:
            emotion_score += row[f'Rank_{rank}_Score']
    return emotion_score

emotions = ['joy', 'surprise', 'fear', 'anger', 'sadness', 'disgust']

for emotion in emotions:
    tm_df[emotion] = tm_df.reset_index(drop=True).copy().swifter\
                            .progress_bar(enable=True, desc=f'Processing {emotion}: ')\
                            .set_npartitions(20)\
                            .allow_dask_on_strings(enable=True)\
                            .apply(extract_emotions, args=tuple([emotion]), axis=1)

scores_columns = ['text','sum_percentages'] + emotions
tm_df[scores_columns].to_parquet('/dlabdata1/smarda/private_data/master/torchmoji_cumulative_scores.parquet.gzip', compression='gzip')


# Add scores to original master dataframe
df = df.reset_index(drop=True)
tm_df = tm_df.reset_index(drop=True)
for emotion in emotions:
    df[emotion] = tm_df[emotion].copy()
df.to_parquet('/dlabdata1/smarda/private_data/master/tweets_with_scores.parquet.gzip', compression='gzip')