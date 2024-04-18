# Code for data scraping
from bs4 import BeautifulSoup
import requests
import pandas as pd

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
print(df)
                       
    

