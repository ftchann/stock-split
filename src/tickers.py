from sre_parse import CATEGORIES

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.splithistory.com/"
CATEGORIES = ["consumer", "energy", "financial", "healthcare", "industrial", "materials", "services",
              "technology", "utilities", "miscellaneous"]


def get_tickers():
    """
    Get all tickers from the website
    """
    tickers = set()
    for category in CATEGORIES:
        url = BASE_URL + category
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        elem = soup \
            .body \
            .center \
            .find('div', style="border: 1px solid #444444; background: #FFFFFF; width:1000px;") \
            .find('table', border="0", style="") \
            .find('tr') \
            .find('td', width="420")
        for link in elem.find_all('a'):
            ticker_url = link.get('href')
            ticker = ticker_url.split('/')[-2]
            tickers.add(ticker)
    ans = list(tickers)
    ans.sort()
    return ans


if __name__ == '__main__':
    tickers = get_tickers()
    print(len(tickers))
