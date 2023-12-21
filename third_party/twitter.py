# pylint: disable-all

import os
import tweepy
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("twitter")

twitter_client = tweepy.OAuthHandler(
    os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"]
)
twitter_client.set_access_token(
    os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_SECRET"]
)
api = tweepy.API(twitter_client)


def scrape_user_tweets(username, num_tweets=20):

    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """

    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
        tweet_list.append(tweet_dict)

    return tweet_list
