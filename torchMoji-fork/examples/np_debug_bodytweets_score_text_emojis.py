
""" Use torchMoji to score texts for emoji distribution.

The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the torchMoji repo.

Writes the result to a csv file.
"""
from __future__ import print_function, division, unicode_literals
import example_helper
import json
import csv
import numpy as np

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH

OUTPUT_PATH = '/dlabdata1/smarda/private_data/master/all_tweets_master_torchmoji_output-63-maxlen30-debug-np.csv'
OUTPUT_PARQUET_PATH = OUTPUT_PATH[:-4] + '.parquet.gzip'


# --------- This code added for BodyTweets project ---------------
import os
import pandas as pd
from tqdm import tqdm

master_tweets_filepath = '/dlabdata1/smarda/private_data/master/all_tweets_master.parquet.gzip'
SENTENCES = pd.read_parquet(master_tweets_filepath, columns=['tweet_text'])['tweet_text'].tolist()
SENTENCES_BATCH_SIZE = 1000

NUM_OUTPUT_VARS = 64

# All code below this line is from the original torchMoji
# except for TEST_SENTENCES = ...

'''
TEST_SENTENCES = ['I love mom\'s cooking',
                  'I love how you never reply back..',
                  'I love cruising with my homies',
                  'I love messing with yo mind!!',
                  'I love you and now you\'re just gone..',
                  'This is shit',
                  'This is the shit'
                  'I love you and now you\'re just gone..'*20]
sentences = TEST_SENTENCES
'''
# ---------- End BodyTweets Project Modifications ----------------------

def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]

maxlen = 300

print('Tokenizing using dictionary from {}'.format(VOCAB_PATH))
with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)


print('Loading model from {}.'.format(PRETRAINED_PATH))
model = torchmoji_emojis(PRETRAINED_PATH)
print(model)

st = SentenceTokenizer(vocabulary, maxlen)

def run_predictions(df, sentences):
    print('Running predictions.')
    tokenized, _, _ = st.tokenize_sentences(sentences)
    prob = model(tokenized)

    for prob in [prob]:
        # Find top emojis for each sentence. Emoji ids (0-63)
        # correspond to the mapping in emoji_overview.png
        # at the root of the torchMoji repo.
        print('Writing results to {}'.format(OUTPUT_PATH))
        scores = []
        #for i, t in tqdm(enumerate(sentences), desc='Processing this batch', total=len(sentences)):
        for i, t in tqdm(enumerate(sentences), desc='Processing this batch', total=len(sentences)):
            t_tokens = tokenized[i]
            t_score = [t]
            t_prob = prob[i]
            ind_top = top_elements(t_prob, NUM_OUTPUT_VARS)
            t_score.append(sum(t_prob[ind_top]))
            t_score.extend(ind_top)
            t_score.extend([t_prob[ind] for ind in ind_top])
            #batch_arr = np.append(np.array(scores))
            scores.append(t_score)
        try:
            batch_arr = np.append(batch_arr, np.array(scores), axis=0)
        except (ValueError, UnboundLocalError): # array hasn't been created yet
            batch_arr = np.array(scores)

        df = df.append(pd.DataFrame(batch_arr, columns=df.columns))
        '''
        with open(OUTPUT_PATH, 'a', encoding='utf-16') as csvfile:
            #writer = csv.writer(csvfile, delimiter=str(','), lineterminator='\n')
            #writer.writerow(['Text', 'Top5%',
            #                'Emoji_1', 'Emoji_2', 'Emoji_3', 'Emoji_4', 'Emoji_5',
            #                'Pct_1', 'Pct_2', 'Pct_3', 'Pct_4', 'Pct_5'])
            for i, row in tqdm(enumerate(scores), desc='Saving this batch', total=len(scores)):
                try:
                    #writer.writerow(row)
                    df = df.append(pd.Series(row, index=df.columns), ignore_index=True)
                except Exception as e:
                    print("Exception at row {}!".format(i))
                    print(e)
        '''            
    return df

if __name__ == '__main__':
    columns = ['text','sum_percentages'] + [f'Rank_{rank}_Emoji' for rank in range(1,NUM_OUTPUT_VARS+1)]\
        + [f'Rank_{rank}_Score' for rank in range(1, NUM_OUTPUT_VARS+1)]
    df = pd.DataFrame(columns=columns)
    desc = 'Processing sentences in batches: '
    for start_idx in tqdm(range(0, len(SENTENCES), SENTENCES_BATCH_SIZE), desc=desc):
        df = run_predictions(df, SENTENCES[start_idx:start_idx + SENTENCES_BATCH_SIZE])

    # Delete if file doesn't exist 
    try:
        os.remove(OUTPUT_PARQUET_PATH)
    except OSError:
        pass
    df.to_parquet(OUTPUT_PARQUET_PATH, compression='gzip')