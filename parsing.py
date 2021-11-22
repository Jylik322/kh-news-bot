import requests
import os
from bs4 import BeautifulSoup
from requests.api import head, post
import cssutils
URL = 'http://innovations.kh.ua/khnews/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://auto.ria.com'

class Post:
    post_Title = ''
    post_Date = ''
    post_Link = ''
    post_Heading = ''
    post_ShortDesc = ''
    def __init__(self, title, date, link, heading, desc) -> None:
        self.post_Title = title
        self.post_Date = date
        self.post_Link = link
        self.post_Heading = heading
        self.post_ShortDesc = desc
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    #find all posts
    postsInner = soup.find('div','mg-posts-sec-inner')
    postsInfos = postsInner.findChildren("div", class_='mg-sec-top-post py-3 col')
    posts = []
    for post in postsInfos:
        posts.append(post)
    print(str(len(posts))+" POSTS")
    #FIND HEADING
    headings = []
    for heading in posts:
        a_class = heading.findChild('a','newsup-categories category-color-1')
        headings.append(a_class.getText())
    print(str(len(headings))+'HEADINGS')
    #FIND DESCRIPTION
    descriptions = []
    for description in posts:
        desc_div = description.findChild('div','mg-content')
        descriptions.append(desc_div.findChild('p').getText())
        print(desc_div.findChild('p').getText())
    print(str(len(headings))+'HEADINGS')
    #FIND DATE
    dates = []
    spans = []
    for parent in posts:
        spans.append(parent.findChild('span', class_='mg-blog-date'))
    for date in spans:
        dateElem = date.findChild("a", href=True).getText()
        print(dateElem)
        if dateElem.find(','):
            dates.append(dateElem)
    print(str(len(dates))+ "DATES")
    #FIND TITLE
    titles = []
    links = []
    a = []
    for parent in posts:
        a.append(parent.findChild('h4', class_='entry-title title'))
    for tags in a:
        tag = tags.findChild('a', href = True)
        titles.append(tag.getText())
        links.append(tag['href'])
    print(str(len(titles))+ "TITLES")
    print(str(len(links))+ "LINKS")
    #CREATE NEWS CLASSES
    news = []
    n =0
    for i in range(len(titles)):
        news.append(Post(titles[n],dates[n].strip(),links[n],headings[i].strip(),descriptions[i]))
        n+=1
    return news
    
  
    

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        news = get_content(html.text)
    else:
        print('Error')
    return news