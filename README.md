# BodyTweets

Welcome! This repository contains the relevant code for the paper "BodyTweets: Foundations for Social Media Analysis of Body-Based Language". This was a thesis paper for the MSc in Data Science at EPFL in Lausanne, Switzerland. The project collects and discusses a custom dataset of (text-based, not image-based) body shaming on Twitter. It geolocates these Tweets using user-string based geolocation, then assesses emotion content using the HuggingFace [DeepMoji](https://github.com/bfelbo/DeepMoji) tool and correlates the output to demographic data taken from the [American Community Survey](https://www.census.gov/programs-surveys/acs). 

For the paper, see [report.pdf](report.pdf). Regarding code, the bulk of the data acquisition and processing scripts can be found in the [tweets_code](tweets_code) directory. In separate files, this directory contains Python code for:

- querying the Twitter API (both in [single-batch form](tweets_code/get_tweets.py) and [continuous-loop form](tweets_code/get_tweets_loop.py))
- [timing and error-handling of requests](tweets_code/request_management.py)
- [organizing the raw API response into organized pandas DataFrames](tweets_code/read_tweets.py)
- [geolocating the tweets using the algorithm in the report (`geolocation.py`)](tweets_code/geolocation.py), including parallelization for the computationally- intensive string processing

The [analysis](analysis) directory contains the code for the dataset and emotion analysis discussed in chapters 4-6 of the report. 

### Collected Dataset

The dataset can be found in the [public_data](public_data) folder in the file [`final_tweet_id_list.csv`](public_data/final_tweet_id_list.csv). The Twitter API User Agreement prohibits publication of any further information beyond the tweet IDs, but information about the tweets including the user ID, timestamp, and content can be re-retrieved using the [Twitter API](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/quick-start).

For any further questions, please feel free to contact me at: X.Y<span>@</span>alumni.epfl.ch with X=daniel and Y=smarda. Project Supervised by [Navid Rekabsaz - JKU, Austria](https://www.jku.at/en/institute-of-computational-perception/about-us/people/navid-rekab-saz/) and [Robert West - dlab, EPFL] (https://dlab.epfl.ch/people/west/).
