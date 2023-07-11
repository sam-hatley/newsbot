import mastodon
from mastodon import Mastodon

from bs4 import BeautifulSoup as bs

from time import sleep
from random import randint
import requests
import json
from os import getenv

## Utilities
def random_header() -> str:
    """
    Returns a random useragent header.
    """
    
    headers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    ]
    
    random_number = randint(0, len(headers) - 1)
    
    return headers[random_number]


def get_mastodon_id(mastodon_address:str) -> str:
    """
    A quick bit of code to fetch a mastodon user's id.
    Usage: get_mastodon_id(mastodon_address='@username@instance.tld') or
    get_mastodon_id(mastodon_address='123456789123456789')
    """
    
    if mastodon_address.isdigit():
        return mastodon_address
    else:
        split_address = mastodon_address.split("@")
        username = split_address[1]
        instance = split_address[2]
        
        url = f"https://{instance}/api/v1/accounts/lookup?acct={username}"
        response = requests.get(url=url)
        response_dict = json.loads(response.text)
        
        return response_dict['id']


## Scraper
def scrape_page(url):
    """
    Uses the requests library to scrape a specified URL. Returns a soup output.
    """
    
    headers = {"User-Agent": random_header()}
    page = requests.get(url=url, headers=headers)
    soup = bs(page.content, "html.parser")
    
    return soup


def scrape_harrow_online(url='https://harrowonline.org/category/news/') -> list[dict]:
    """
    Parses a url from harrow online. Returns category, title, and url of the top
    five articles as a list of dictionaries.
    """
    
    articles = []

    soup = scrape_page(url)
    cards = soup.find_all("div", class_="td-module-container td-category-pos-above")

    for i in cards:
        title = i.find("a", class_="td-image-wrap").attrs['title']
        url = i.find("a", class_="td-image-wrap").attrs['href']
        category = i.find("a", class_="td-post-category").text
        
        article = {
            'category': category,
            'title': title,
            'url': url
        }
        
        articles.append(article)
    
    return articles


# Filter
def filter_articles(user_id,
                    access_token,
                    articles,
                    limit=10,
                    api_base_url='https://mastodon.social') -> list[dict]:
    """
    Takes a list of dictionaries of articles with a URL key, and compares them to the last `limit`
    number of posts by `user_id`. Returns a list of posts that have URLs not within that user's
    posts.
    """

    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=api_base_url
    )
    
    # Retreive links already posted to mastodon
    prior_links = []

    statuses = Mastodon.account_statuses(
        mastodon, 
        id=user_id,
        exclude_replies=True,
        exclude_reblogs=True,
        limit=limit
        )

    for status in statuses:
        soup = bs(status.content, "html.parser")
        tags = soup.find_all('a')
        for tag in tags:
            if tag.get('class') is None:
                link = tag.get('href')
                prior_links.append(link)
            
    
    # Return new articles
    new_posts = []
    for article in articles:
        if article['url'] not in prior_links:
            new_posts.append(article)
    
    return new_posts


# Poster
def create_post(access_token,
                articles,
                api_base_url='https://mastodon.social'
                ) -> list[dict]:
    """
    Takes a list of dictionaries of articles with the keys 'category', 'title', and 'url', and
    posts them to mastodon. Returns articles posted.
    """

    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=api_base_url
    )
    
    # Post new articles to mastodon
    for index, post in enumerate(articles):
        if post['category']:
            category = post['category'].replace(" ", "")
        else:
            category = "News"
        title = post['title']
        url = post['url']
        
        # Get the location
        locations = [
            "Pinner",
            "Edgware",
            "Harrow Weald",
            "Wembley",
            "Wembley Park",
            "Stanmore",
            "Wealdstone",
            "Rayners Lane",
            "North Harrow",
            "South Harrow",
            "Hatch End",
            "Watford",
            "Northolt",
            "Barnet",
        ]
        
        find_location = lambda x: \
            next((location for location in locations if location in x), "Harrow")
        
        location = find_location(title).replace(" ", "")

        # Ensure message length is within limit
        LIMIT = 500
        
        # URLs are always counted as 23 characters, plus add'l chars
        status = f"{title}\n#{location} #{category} #Harrow\n{url}"
        post_length = len(status) - len(url) + 23

        if post_length > LIMIT:
            n = LIMIT - post_length + len(title) - 3
            title = title[:n] + "..."
            status = f"{title}\n#{location} #{category} #Harrow\n{url}"
            print(len(status) - len(url) + 23)

        print(category, title, url)
        
        Mastodon.status_post(
            mastodon,
            status=status
        )
        
        # Rate limiting
        if len(articles) > 1 and index + 1 < len(articles):
            sleep(1)
    
    return articles


def main(data=None, context=None, **kwargs) -> None:
    """
    Main function, calling each of the above functions. Arguments are dummies, as a quirk of
    Google Cloud Functions means that a pub/sub trigger forces arguments.
    """
    # Setup
    access_token = getenv("MASTODON_TOKEN")
    user_id_env = getenv("MASTODON_ID")
    
    if not access_token or not user_id_env:
        raise ValueError("Missing Mastodon access token or user ID in env")
    
    user_id = get_mastodon_id(user_id_env)
    
    # Function
    articles = scrape_harrow_online()
    
    new_posts = filter_articles(user_id=user_id,
                                access_token=access_token,
                                articles=articles)
    
    if new_posts:
        create_post(access_token=access_token,
                    articles=new_posts)
    

if __name__ == "__main__":
    main()
    