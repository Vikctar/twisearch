import tweepy
import sys
import os
import csv
from time import asctime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

headers = [
    'created_at', 'text', 'url', 'source', 'retweet_count', 'favorite_count',
    'truncated', 'geo', 'place', 'user_name', 'user_screen_name',
    'user_location', 'user_description', 'user_followers_count', 'user_friends_count',
    'user_favorites_count'
]

if not api:
    print("Can't Authenticate")
    sys.exit(-1)

search_query = sys.argv[1] or 'Ronaldo'

day_of_search = '_' + asctime().replace(' ', '_')
max_tweets = 100
tweets_per_query = 100
csv_file = search_query.lower().replace(' ', '_') + day_of_search + '.csv'
csv_file = csv_file.casefold()

since_id = None

tweet_count = 0

max_id = -1

print(f'Downloading max {max_tweets} tweets')

with open(csv_file, 'w', encoding='utf-8') as file:
    while tweet_count < max_tweets:
        writer = csv.writer(file)
        # Column/Header names
        writer.writerow(headers)
        try:
            if max_id <= 0:
                if not since_id:
                    new_tweets = api.search(q=search_query, count=tweets_per_query, tweet_mode='extended')
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_query, since_id=since_id,
                                            tweet_mode='extended')

            else:
                if not since_id:
                    new_tweets = api.search(q=search_query, count=tweets_per_query, max_id=str(max_id - 1),
                                            since_id=since_id, tweet_mode='extended')
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_query, max_id=str(max_id - 1),
                                            since_id=since_id, tweet_mode='extended')

            if not new_tweets:
                print('No more tweets found')
                break

            for tweet in new_tweets:
                if 'retweeted_status' in tweet._json:
                    screen_name = tweet._json['user']['screen_name']
                    retweet = 'RT @' + screen_name + ':'
                    full_text = retweet + tweet._json['retweeted_status']['full_text']
                    url = f'https://twitter.com/twitter/status/{tweet._json.get("id_str")}'

                    writer.writerow(
                        [
                            tweet._json['created_at'], full_text, url, tweet.source,
                            tweet.retweet_count, tweet.favorite_count, tweet.truncated, tweet.geo,
                            tweet.place, tweet._json['user']['name'], tweet._json['user']['screen_name'],
                            tweet._json['user']['location'], tweet._json['user']['description'],
                            tweet._json['user']['followers_count'], tweet._json['user']['friends_count'],
                            tweet._json['user']['favourites_count']
                        ]
                    )
                else:
                    _url = f'https://twitter.com/twitter/status/{tweet._json.get("id_str")}'
                    writer.writerow(
                        [
                            tweet._json['created_at'], tweet.full_text, _url, tweet.source,
                            tweet.retweet_count, tweet.favorite_count, tweet.truncated, tweet.geo,
                            tweet.place, tweet._json['user']['name'], tweet._json['user']['screen_name'],
                            tweet._json['user']['location'], tweet._json['user']['description'],
                            tweet._json['user']['followers_count'], tweet._json['user']['friends_count'],
                            tweet._json['user']['favourites_count']
                        ]
                    )

            tweet_count += len(new_tweets)
            print(f'Downloaded {tweet_count} tweets')
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            print('An error occured: ' + str(e))
            break

print(f'Downloaded {tweet_count} tweets, saved to {csv_file}')
