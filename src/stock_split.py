import json
import re
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

import tickers

BASE_URL = "https://www.splithistory.com/"


def get_stock_split_history(ticker):
    """
    Get stock split history for a given ticker.
    """
    url = BASE_URL + ticker
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    elems = soup \
        .body \
        .center \
        .find('div', style="border: 1px solid #444444; background: #FFFFFF; width:1000px;") \
        .find('table', border="0", style="") \
        .find_all('tr')
    splits = []
    pattern = "(\d+) for (\d+)"
    prog = re.compile(pattern)
    for elem in elems:
        row = elem.find_all('td', align="center", style="padding: 4px; border-bottom: 1px solid #CCCCCC")
        if row:
            date = row[0].text
            ratio = row[1].text
            result = prog.match(ratio)
            if result:
                split = {}
                split['date'] = date
                split['ratio_in'] = int(result.group(1))
                split['ratio_out'] = int(result.group(2))
                splits.append(split)
    stock = {'ticker': ticker, 'splits': splits}
    return stock


def get_all_stock_split_histories(tickers):
    """
    Get stock split history for all tickers.
    """
    # Get stock split history for each ticker
    stocks = []
    executor = ThreadPoolExecutor(max_workers=10)
    tasks = []
    for ticker in tickers:
        # Get stock split history
        task = executor.submit(get_stock_split_history, ticker)
        tasks.append(task)
    for task in tasks:
        res = task.result()
        stocks.append(res)
    return stocks


if __name__ == '__main__':
    tickers = ["AAPL", "AMZN", "FB", "GOOG", "MSFT", "NFLX", "TSLA"]
    history = get_all_stock_split_histories(tickers)
    print("hello")
    with open('result/stock_split_history.json', 'w') as f:
        json_string = json.dumps(history, indent=4)
        f.write(json_string)