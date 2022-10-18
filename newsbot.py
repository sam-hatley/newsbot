import tweepy
import re
import requests
from bs4 import BeautifulSoup
import config

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_secret)

client = tweepy.Client(bearer_token=config.bearer_token)

tweets = client.search_recent_tweets(query='from:harrowonline',
                                     tweet_fields=['context_annotations', 'created_at'],
                                     max_results=10)

for tweet in tweets.data:
    datetime = tweet.created_at
    text = tweet.text
    url = re.findall('(?P<url>https?://[^\s]+)', text)
    if url != []:
        url = url[0]
        get_url = requests.get(url)
        get_text = get_url.text
        soup = BeautifulSoup(get_text, "html.parser")
        title = soup.find_next('h1', 'class:tdb-title-text')
        print(title)


# ['__abstractmethods__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__',
# '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__',
# '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
# '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_abc_impl',
# 'attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'data', 'entities', 'geo',
# 'get', 'id', 'in_reply_to_user_id', 'items', 'keys', 'lang', 'non_public_metrics', 'organic_metrics',
# 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'source',
# 'text', 'values', 'withheld']
