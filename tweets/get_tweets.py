from twarc import Twarc2, expansions
import datetime
import json

settings_file = json.load(open("settings.json"))
# Replace your bearer token below
client = Twarc2(bearer_token=settings_file["bearer_token"])


def main():
    # Specify the start time in UTC for the time period you want Tweets from
    start_time = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    # Specify the end time in UTC for the time period you want Tweets from
    end_time = datetime.datetime(2021, 5, 30, 0, 0, 0, 0, datetime.timezone.utc)

    # This is where we specify our query as discussed in module 5
    query = "from:twitterdev"

    # The counts_all method call the full-archive Tweet counts endpoint to get Tweet volume based on the query, start and end times
    search_results = client.search_all(query=query, start_time=start_time, end_time=end_time, max_results=0)

    # Twarc returns all Tweet counts for the criteria set above, so we page through the results
    for page in search_results:
        result = expansions.flatten(page)
        with open('downloaded_tweets.json', 'w') as f:
            for tweet in result:
                json.dump(tweet, f, ensure_ascii=False, indent=4)
        break

    
if __name__ == "__main__":
    main()