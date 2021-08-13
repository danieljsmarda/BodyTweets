import json
import swifter
import pandas as pd

input_path = '/dlabdata1/smarda/private_data/master/all_tweets_master_torchmoji_output-63-maxlen30-debug-np.parquet.gzip'
tm_df = pd.read_parquet(input_path)

num_scores = 64
score_cols = [f'Rank_{i}_Score' for i in range(1, num_scores+1)]
from tqdm import tqdm
for col_name in tqdm(score_cols, desc='Converting Types: '):
    tm_df[col_name] = pd.to_numeric(tm_df[col_name])

def extract_emotions_return_df(row, target_emotions):
    output_row = pd.Series(index=[f'Total_{emotion}_Score' for emotion in target_emotions])
    emotion_scores = {emotion:0 for emotion in target_emotions}
    for rank in range(1, num_scores+1):
        emoji_idx = row[f'Rank_{rank}_Emoji']
        score = row[f'Rank_{rank}_Score']
        emotion = emoji_mappings[emoji_idx]
        output_row[f'Total_{emotion}_Score'] += score
    return output_row

emotion_scores_df = tm_df.reset_index(drop=True).copy().swifter\
                            .progress_bar(enable=True, desc=f'Processing all emotions: ')\
                            .set_npartitions(20)\
                            .allow_dask_on_strings(enable=True)\
                            .apply(extract_emotions_return_df, args=[emotions], axis=1)
                            