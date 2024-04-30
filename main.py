#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import json

class BBC:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        
    def get_body(self) -> list:
        body = self.soup.find(property="articleBody")
        return [p.text for p in body.find_all("p")]
    
    def get_title(self) -> str:
        return self.soup.find(class_="story-body__h1").text

# # Create a dictionary 
# URL = [
#     ("https://www.aljazeera.com/", "Al Jazeera"),
#     ("https://www.bbc.com/news", "BBC"),
#     # ("https://www.reuters.com/", "Reuters"),
#     # ("https://www.scmp.com/", "SCMP"),
#     # ("https://apnews.com/world-news", "AP News")
#        ]

# news = []
# # HTTP Get request to website
# for url, source in URL:
#     r = requests.get(url)
#     # print(r.content)

# # Parse content
#     soup = BeautifulSoup(r.content, 'html.parser')

#     # Get relevant information from the website
    
#     articlelist = soup.find_all('article')
#     # count = 0
#     for article in articlelist:
#         link = article.find('a', href = True)
#         if link:
#             news.append((source, link['href']))

#             # count += 1
#             # if count == 3:
#             #     break
# #     news.append(articlelist)
# #to limit to 3 articles
# # news = news[:3]
# # remove duplicates
# # news = list(set(news))
# # news = news[:12]

# # print(news)
# # # Put article data in a csv to check above fn works
# # df = pd.DataFrame(news)
# # df.to_csv (r'C:\Users\meimeixu@Zhimeis-MacBook-Pro\Downloads\news.csv', index = False, header = True)

# data = json.loads(soup.select_one("#__NEXT_DATA__").text)

# def extract_title(news):
#     extracted = []
#     # Define the pattern to match the date and title
#     for name, link in news:
    
#         if name == "Al Jazeera":
            
#             pattern = r"/news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<title>[\w-]+)"
#             # print(link)
#             match = re.match(pattern, link)
            
#             if match:
#                 # Extract the matched groups
#                 title = match.group('title').replace('-', ' ')
#                 extracted.append(title)
#             # else:
#             #     return None

#         if name == "BBC":
#             page = next(
#                 v for k, v in data["props"]["pageProps"]["page"].items() if k.startswith("@"))
#             for c in page["contents"]:
#                 match c["type"]:
#                     case "headline":
#                         print(c["model"]["blocks"][0]["model"]["text"])
#             print()
#     return extracted
#     # # elif "bbc.com" in link:
#     # #     pattern = r"/" # The URL doesn't contain the title
#     # # elif "reuters.com" in link:
#     # #     pattern = r"/(?P<desk>)/(?P<region>)/(?P<title>[w-]+)-2024-04-26/"
#     # # elif "scmp.com" in link:
#     # #     pattern = r"news/china/diplomacy/article/3260454/(?P<title>[w-]+)g?module=top_story&pgtype=homepage"
    
#     # # Use regular expression to find matches
#     #         
    
# title = extract_title(news)
# print(title)
# # def extract_title(link):

# #     for i in df['0']: # needs to be fixed so that we're not using df and so that 'link' works
# #         date, title = extract_date_and_title(i)
        
# #         if date and title:
# #             print("Date:", date)
# #             print("Title:", title)
# #         else:
# #             print("Invalid link format.")
        
# def send_email(subject, body):
#     from_email = "your_email@gmail.com"  # Update with your email
#     to_email = "recipient_email@example.com"  # Update with recipient's email
#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['To'] = to_email
#     msg['Subject'] = subject

# #     msg.attach(MIMEText(body, 'plain'))

# #     server = smtplib.SMTP('smtp.gmail.com', 587)
# #     server.starttls()
# #     server.login(from_email, "your_password")  # Update with your password
# #     text = msg.as_string()
# #     server.sendmail(from_email, to_email, text)
# #     server.quit()
    
# def compose_email_body(df):
#     body = "Today's News Headlines:\n\n Today is ['date']. Here are the top stories from around the world."
#     for index, row in df.iterrows():
#          body += f"{row['date']}: {row['title']}\n"
# #     return body

# # # Function to fetch news, compose email body, and send email
# def send_news_email():
#     body = compose_email_body(df)
#     send_email("Daily News Digest", body)


# # # Schedule to fetch news and send email daily at 8 AM
# schedule.every().day.at("08:00").do(send_news_email)

# while True:
#     schedule.run_pending()
#     time.sleep(1)



    

