# BodyTweets

Welcome. This repository contains the relevant code for the paper "BodyTweets: Foundations for Social Media Analysis of Body-Based Language". This was a thesis paper for the MSc in Data Science at EPFL in Lausanne, Switzerland. You can find the report at [report.pdf](report.pdf). The rough structure of the repo is as follows.

The bulk of the data acquisition and processing code can be found in the [tweets_code](tweets_code) directory. In separate files, this directory contains python scripts for:

- querying the Twitter API (both in [single-batch form](tweets_code/get_tweets.py) and [continuous-loop-form](tweets_code/get_tweets_loop.py))
- [processing errors and timing in requests](tweets_code/request_management.py)
- [organizing the raw-API response into organized pandas DataFrames](tweets_code/read_tweets.py)
- [geolocating the tweets using the algorithm in the report (geolocation.py)](tweets_code/geolocation.py), including parallelization for the computation-intensive string processing

The [analysis](analys9s) directory contains the code for the dataset and emotion analysis discussed in chapters 4-6 of the report. 

For any further questions, please feel free to contact the author (Daniel Smarda) at: X.Y@alumni.epfl.ch with X=daniel and Y=smarda