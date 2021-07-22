with open('tweets/downloaded_tweets.txt', 'r', encoding='utf-16') as f:
    while True:
        d = eval(eval(f.readline()))
        for tweet in d['data']:
            print(tweet['text'])