import tweepy
from datetime import datetime, timedelta
import re
import requests
from bs4 import BeautifulSoup
import config

# Authorisation and login
auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_secret)
client = tweepy.Client(bearer_token=config.bearer_token)

# Get current time and define the range to search
current_date = datetime.now()


# Function to retrieve tweets
def get_tweets(h=1, m=0, user=153798942):
    titles = []
    urls = []

    # Use the input to define number of hours to search from
    time_range = current_date - timedelta(hours=h, minutes=m)

    # The actual query: getting tweets from harrowonline within our predefined
    # time range. Because this query is so specific, we don't really need other
    # filters or information.
    tweets = client.get_users_tweets(id=user,
                                     start_time=time_range,
                                     exclude='retweets')

    # If there are no tweets within time period, exit
    if tweets.data is None:
        exit()

    # Iterate through each tweet
    for tweet in tweets.data:
        text = tweet.text

        # Search for a URL, if there is one, return the first instance
        url = re.findall('(?P<url>https?://[^\s]+)', text)
        if url != []:
            url = url[0]
            get_url = requests.get(url)
            get_text = get_url.text
            soup = BeautifulSoup(get_text, "html.parser")

            # Extract the header from the linked article.
            # Links leading back to twitter cause issues, so we "try" instead
            try:
                title = soup.select('h1.tdb-title-text')[0].text.strip()
            except:
                continue

            # Append these values to a list
            titles.append(title)
            urls.append(url)

    return titles, urls


(titles, urls) = get_tweets(24, 0)

print(titles)
