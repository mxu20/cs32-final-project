#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import json

# Create a dictionary of news sites
URL_list = ['https://www.bbc.com/news', 
            'https://www.aljazeera.com/', 
            'https://www.reuters.com/', 
            'https://www.scmp.com/', 
            'https://apnews.com/world-news']

# Parse through BBC articles
class BBC:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.title = self.get_title()

    # Get top three articles off the homepage of the website
    def get_top_articles(self):
        news = []   # Create dictionary to store news articles
        article_elements = self.soup.find_all('article', limit=3)
        for item in article_elements:
            for link in item.find_all('a', href = True):
                news.append(link['href'])
        top_titles = list(set(news))
        return top_titles
        
    # Get the title of each article
    def get_title(self) -> str:
        title_element = self.soup.find(class_="story-body__h1")
        if title_element is not None:
            return title_element.text
        else:
            print("Title Not Found")

    

# Parse through Al Jazeera articles
class AlJazeera:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.title = self.get_title(url)

    # Get top three articles off the homepage of the website
    def get_top_articles(self):
        news = []
        article_elements = self.soup.find_all('article', limit=3)
        for item in article_elements:
            for link in item.find_all('a', href = True):
                news.append(link['href'])
        top_titles = list(set(news))
        return top_titles

    # Get the title of each article
    def get_title(self, link:str) -> str:
        self.extracted_titles = []  # Store the extracted titles

        pattern = r"/news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<title>[\w-]+)"
        match = re.match(pattern, link)
            
        if match:
            # Extract the matched groups
            title = match.group('title').replace('-', ' ')
            self.extracted_titles.append(title) # Append the title to a list of extracted titles
            return title
    

# Parse through Reuters articles
class Reuters:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.title = self.get_title()
        
    # Get top three articles off the homepage of the website
    def get_top_articles(self):
        news = []
        article_elements = self.soup.find_all('article', limit=3)
        for item in article_elements:
            for link in item.find_all('a', href = True):
                news.append(link['href'])
        top_titles = list(set(news))
        return top_titles

    # Get the title of each article
    def get_title(self) -> str:
        title_element = self.soup.find(property="og_title")
        if title_element is not None:
            return title_element.text
        else:
            print("Title Not Found")
    
        
# Parse through South China Morning Post articles
class SCMP:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.title = self.get_title()

    # Get top three articles off the homepage of the website
    def get_top_articles(self):
        news = []
        article_elements = self.soup.find_all('article', limit=3)
        for item in article_elements:
            for link in item.find_all('a', href = True):
                news.append(link['href'])
        top_titles = list(set(news))
        return top_titles

    # Get the title of each article
    def get_title(self) -> str:
        title_element = self.soup.select_one('span[data-qa="ContentHeadline-Headline"]')
        
        # Make sure the title element was found before trying to access its text
        if title_element is not None:
            return title_element.text
        else:
            print("Title Not Found")
    

# Parse through AP World News articles
class AP:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.title = self.get_title()

    # Get top three articles off the homepage of the website
    def get_top_articles(self):
        news = []
        article_elements = self.soup.find_all('article', limit=3)
        for item in article_elements:
            for link in item.find_all('a', href = True):
                news.append(link['href'])
        top_titles = list(set(news))
        return top_titles

    # Search for title in HTML code
    def get_title(self) -> str:
        title_element = self.soup.find('h1', class_='Page-headline')
        if title_element is not None:
            return title_element.text
        else:
            print("Title Not Found")

# Create a dictionary of classes
classes_list = [BBC, AlJazeera, Reuters, SCMP, AP]

# Use zip to pair url and corresponding class
for url, NewsWebsite in zip(URL_list, classes_list):
    website = NewsWebsite(url)
    top_titles = website.get_top_articles() # Call the new method
    print(top_titles)

# Put article data in a csv
df = pd.DataFrame(top_titles)
df.to_csv (r'C:\Users\meimeixu@Zhimeis-MacBook-Pro\Downloads\news.csv', index = False, header = True)


# Create newsletter to send to subscriber
def send_email(subject, body):
    from_email = "your_email@gmail.com"  # Update with your email
    to_email = "recipient_email@example.com"  # Update with recipient's email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, "your_password")  # Update with your password
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Compose the text of the newsletter
def compose_email_body(df):
    body = "Today's News Headlines:\n\n Today is ['date']. Here are the top stories from around the world."
    for index, row in df.iterrows():
         body += f"{row['date']}: {row['title']}\n"
#     return body

# # Function to fetch news, compose email body, and send email
def send_news_email():
    body = compose_email_body(df)
    send_email("Daily News Digest", body)


# # Schedule to fetch news and send email daily at 8 AM
schedule.every().day.at("08:00").do(send_news_email)

while True:
    schedule.run_pending()
    time.sleep(1)



