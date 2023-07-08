import mastodon
from mastodon import Mastodon
from bs4 import BeautifulSoup as bs
from time import sleep

from scraper import scrape_harrow_online


def harrow_online_post(user_id,
                       access_token,
                       api_base_url='https://mastodon.social'
                       ) -> list[dict]:

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
        limit=10
        )

    for status in statuses:
        soup = bs(status.content, "html.parser")
        link = soup.find('a')
        if link:
            prior_links.append(link.attrs['href'])
    
    # Grab articles from page
    articles = scrape_harrow_online()
    
    # Return new articles
    new_posts = []
    for article in articles:
        if article['url'] not in prior_links:
            new_posts.append(article)
    
    # Post new articles to mastodon
    if new_posts:
        for index, post in enumerate(new_posts):
            category = post['category']
            title = post['title']
            url = post['url']
            print(category, title, url)
            
            Mastodon.status_post(
                mastodon,
                status=f"""{category.upper()}\n{title}\n{url}"""
            )
            
            # Rate limiting
            if len(new_posts) > 1 and index + 1 < len(new_posts):
                sleep(1)
    
    return new_posts