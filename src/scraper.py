from bs4 import BeautifulSoup as bs
import requests

from utils import random_header


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