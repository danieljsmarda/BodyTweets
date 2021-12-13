Data directory containing all data freely available to public. 

- [`emoji_mappings.json`](emoji_mappings.json) and  [`final_tweet_id_list.csv`](final_tweet_id_list.csv) were manually created specifically for this project.
- The csv files [`canadacensusareas.csv`](https://github.com/danieljsmarda/BodyTweets/blob/main/public_data/canadacensusareas.csv), [`ukcensusareas.csv`](https://github.com/danieljsmarda/BodyTweets/blob/main/public_data/ukcensusareas.csv), [`uncities.csv`](https://github.com/danieljsmarda/BodyTweets/blob/main/public_data/uncities.csv), [`uncountries.csv`](https://github.com/danieljsmarda/BodyTweets/blob/main/public_data/uncountries.csv), [`usacscities.csv`](https://github.com/danieljsmarda/BodyTweets/blob/main/public_data/usacscities.csv), and [`usstateabbreviations.csv`](https://github.com/danieljsmarda/BodyTweets/blob/main/public_data/usstateabbreviations.csv) were downloaded directly from the corresponding public census websites. Reference details are in the report. 
- The `location_data`* files were created using the [python shelve module](https://docs.python.org/3/library/shelve.html) for storing small pandas DataFrames. 

When executing the pipeline, the location csv files are fed into the [external data processing notebook](../tweets_code/external_locations.ipynb) (see the [tweets_code](../tweets_code) folder). This notebook processes these raw spreadsheets into the useable `location_data` DataFrames, which are then loaded and matched to the tweets with the [`geolocation.py`](../tweets_code/geolocation.py) code.

