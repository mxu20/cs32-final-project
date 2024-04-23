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

# HTTP Get request to website
URL = "https://www.aljazeera.com/"
r = requests.get(URL)
print(r.content)

# Parse content
soup = BeautifulSoup(r.content, 'html.parser')

# Get relevant information from the website
news = []
articlelist = soup.find_all('article')

# Loop to find all urls of articles on the front page
for item in articlelist:
    for link in item.find_all('a', href = True):
        news.append(link['href'])
news = list(set(news))

# Put article data in a csv
df = pd.DataFrame(news)
df.to_csv (r'C:\Users\meimeixu@Zhimeis-MacBook-Pro\Downloads\news.csv', index = False, header = True)


def extract_date_and_title(link):
    # Define the pattern to match the date and title
    pattern = r"/news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<title>[\w-]+)"
    
    # Use regular expression to find matches
    match = re.match(pattern, link)
    
    if match:
        # Extract the matched groups
        date = f"{match.group('year')}-{match.group('month')}-{match.group('day')}"
        title = match.group('title').replace('-', ' ')
        return date, title
    else:
        return None, None

for i in df['link']:
    date, title = extract_date_and_title(i)
    
    if date and title:
        print("Date:", date)
        print("Title:", title)
    else:
        print("Invalid link format.")
        
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
    
def compose_email_body(df):
    body = "Today's News Headlines:\n\n" #here she can flesh out the full message
    for index, row in df.iterrows():
        body += f"{row['date']}: {row['title']}\n"
    return body

# Function to fetch news, compose email body, and send email
def send_news_email():
    body = compose_email_body(df)
    send_email("Daily News Digest", body)


# Schedule to fetch news and send email daily at 8 AM
schedule.every().day.at("08:00").do(send_news_email)

while True:
    schedule.run_pending()
    time.sleep(1)
                       
    

