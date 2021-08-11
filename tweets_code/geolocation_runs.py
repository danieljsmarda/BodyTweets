from geolocation import geolocate_tweets
from tqdm import tqdm
import logging


run_dir = '/dlabdata1/smarda/private_data/tweet_collection_runs/Wed Aug 11 12:52:17 2021/'
logging.basicConfig(level=logging.INFO, filename=run_dir + 'geoloc_logfile.log')

if __name__ == '__main__':
    for year in tqdm(['2013', '2015', '2017', '2019', '2021'], desc='Year Loop: '):
        geolocate_tweets(run_dir + 'dump-' + year + '.txt', 
                         run_dir + year + 'all_columns.parquet.gzip',
                         run_dir + year + 'relevant_columns.parquet.gzip'
        )
        