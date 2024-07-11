import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
#from send_message import send_email
import os
import re

def scrape_the_hacker_news():
    # URL of the thehackernews page
    url = "https://thehackernews.com/"

    # Fetch the HTML content from the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Store response content
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the "root" id in the HTML content
        articles_list = soup.find("div", class_="blog-posts clear").find_all("a")

        # Define the regex pattern to match the date format
        date_pattern = r'/i>(.*)</span>'

        for i in articles_list:
            print(i.get("href"))
            print(i.find("h2", class_="home-title").text.strip())

            the_text = str(i.find("span", class_="h-datetime"))
            #print(type(the_text))

            # Search for the pattern in the HTML content
            match = re.search(date_pattern, the_text)

            if match:
                
                print(match.group(1).strip())



        

def main():
    scrape_the_hacker_news()

if __name__ == "__main__":
    main()