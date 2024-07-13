import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
#from send_message import send_email
import os
import re

# Function to load data from a CSV file
def load_data_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"missing {filename} file")
    
# Function to append data to a CSV file
def append_data_to_csv(df, file_path):
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def scrape_the_hacker_news(keywords_df):
    # URL of the thehackernews page
    url = "https://thehackernews.com/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Fetch the HTML content from the URL
    response = requests.get(url, headers=headers)

    article_data = []

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

            article_dict = {}

            for keyword in keywords_df['keywords'].tolist():

                if keyword in i.find("h2", class_="home-title").text.strip() or keyword in i.find("div", class_="home-desc").text.strip():

                    article_dict["source"] = "the hacker news"

                    article_dict["keyword"] = keyword

                    #print(i.find("h2", class_="home-title").text.strip())
                    article_dict["title"] = i.find("h2", class_="home-title").text.strip()

                    #print(i.get("href"))
                    article_dict["article_link"] = i.get("href")

                    the_text = str(i.find("span", class_="h-datetime"))
                    #print(type(the_text))

                    # Search for the pattern in the HTML content
                    match = re.search(date_pattern, the_text)

                    if match:
                        
                        #print(match.group(1).strip())
                        article_dict["date"] = match.group(1).strip()

                    #print(i.find("div", class_="home-desc").text.strip())
                    article_dict["description"] = i.find("div", class_="home-desc").text.strip()

                    article_data.append(article_dict)

    #print(article_data)
    return(article_data)

def scrape_security_week(keywords_df):
    # URL of the securityweek page
    url = "https://www.securityweek.com/category/vulnerabilities/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Fetch the HTML content from the URL
    response = requests.get(url, headers=headers)

    article_data = []

    if response.status_code == 200:
        # Store response content
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the "root" id in the HTML content
        articles = soup.find('div', id='zox-home-main-wrap', class_='zoxrel zox100')

        #links = articles_list.find_all('a', href=True, rel="bookmark", 'h2')

        articles_list = articles.find_all('div', class_="zox-art-title")

        for i in articles_list:

            article_dict = {}

            for keyword in keywords_df['keywords'].tolist():

                if keyword in i.find("a").find("h2").text.strip():

                    article_dict["source"] = "security week"

                    article_dict["keyword"] = keyword

                    article_dict["title"] = i.find("a").find("h2").text.strip()

                    article_dict["article_link"] = i.find("a").get("href")

                    article_dict["date"] = ""

                    article_dict["description"] = i.find("a").find("h2").text.strip()

                    article_data.append(article_dict)

        return article_data
    
def scrape_cybersecurity_news(keywords_df):
    # URL of the securityweek page
    url = "https://cybersecuritynews.com/category/vulnerability/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Fetch the HTML content from the URL
    response = requests.get(url, headers=headers)

    article_data = []

    if response.status_code == 200:
        # Store response content
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the "root" id in the HTML content
        articles = soup.find('div', class_='td-main-content-wrap td-container-wrap')

        articles_list = articles.find_all("div", class_="td_module_11 td_module_wrap td-animation-stack")

        for i in articles_list:

            article_dict = {}

            for keyword in keywords_df['keywords'].tolist():

                if keyword in i.find("h3", class_="entry-title td-module-title").text.strip() or keyword in i.find("div", class_="td-excerpt").text.strip():

                    article_dict["source"] = "cybersecurity news"

                    article_dict["keyword"] = keyword

                    article_dict["title"] = i.find("h3", class_="entry-title td-module-title").text.strip()

                    article_dict["article_link"] = i.find("h3", class_="entry-title td-module-title").find("a").get("href")

                    article_dict["date"] = i.find("time", class_="entry-date updated td-module-date").text.strip()

                    article_dict["description"] = i.find("div", class_="td-excerpt").text.strip()

                    article_data.append(article_dict)


        return article_data

        
def main():

    keywords_csv = "keywords.csv"

    data_csv = "data.csv"

    keywords_df = load_data_from_csv(keywords_csv)

    data_df = load_data_from_csv(data_csv)

    the_hacker_news_output = scrape_the_hacker_news(keywords_df)

    the_security_week = scrape_security_week(keywords_df)

    cybersecurity_news = scrape_cybersecurity_news(keywords_df)

    if the_hacker_news_output:
        for i in the_hacker_news_output:
            if i["article_link"] not in data_df['article_link'].tolist():
                new_row = pd.DataFrame([i])
                append_data_to_csv(new_row, data_csv)

    if the_security_week:
        for i in the_security_week:
            if i["article_link"] not in data_df['article_link'].tolist():
                new_row = pd.DataFrame([i])
                append_data_to_csv(new_row, data_csv)

    
    if cybersecurity_news:
        for i in cybersecurity_news:
            if i["article_link"] not in data_df['article_link'].tolist():
                new_row = pd.DataFrame([i])
                append_data_to_csv(new_row, data_csv)


if __name__ == "__main__":
    main()