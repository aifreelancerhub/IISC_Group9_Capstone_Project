import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class NewsScraper:
    def __init__(self):
        self.nifty_companies = [
            "Reliance Industries", "TCS", "Infosys", "HDFC Bank", "ICICI Bank",
            "Hindustan Unilever", "SBI", "Bharti Airtel", "Kotak Mahindra Bank",
            "Adani Enterprises", "ITC", "HCL Technologies", "Axis Bank",
            "Larsen & Toubro", "Bajaj Finance", "Nestle India", "Wipro",
            "Asian Paints", "Maruti Suzuki", "Titan Company"
        ]
        self.news_url = (
            "https://www.google.com/search?sca_esv=0779345a01e3fcf7&sxsrf=ADLYWIKkyZoODP9NCxwD4f1Yp9S7uVoL4w:1732958682800&q={company}+stock+news&tbm=nws&source=lnms"
        )
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
        }
        
    def fetch_news(self):
        news_list = []

        for company in self.nifty_companies:
            # Format the search URL for the company
            url = self.news_url.format(company=company.replace(" ", "+"))
            
            # Send the request with headers
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Failed to fetch news for {company}. Status code: {response.status_code}")
                continue

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the 'search' div that contains news results
            search_div = soup.find('div', {'id': 'search'})
            
            if search_div:
                # Extract the text from each div inside the 'search' div
                div_text = ''
                # for div in search_div.find_all('div'):
                div_text= search_div.get_text(separator=' ', strip=True) + ' '
                news_list.append({
                    "company": company,
                    "news": div_text.strip(),
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                news_list.append({
                    "company": company,
                    "news": "No news found",
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Return the news list as a DataFrame
        return pd.DataFrame(news_list)

'''
# Create an instance of the NewsScraper class and fetch the news
news_scraper = NewsScraper()
news_df = news_scraper.fetch_news()

# Print the result
print(news_df)'''
