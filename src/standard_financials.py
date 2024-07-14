from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_tickers():
    # get all tickers to initialise the database
    # for now, just doing s&p, can expand all tickers later
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        if ticker == 'FB':
            ticker = 'META'

        tickers.append(ticker)

    return tickers


def get_driver(showGui=False):
    options = Options()

    if not showGui:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1920, 1080)

    return driver


def handle_cookies(driver):
    try:
        consent_overlay = WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.consent-overlay')))

        accept_all_button = consent_overlay.find_element(By.CSS_SELECTOR, '.accept-all')
        accept_all_button.click()

        return

    except TimeoutException:
        return


def financial_data_points(driver, ticker):
    driver.get(f"https://finance.yahoo.com/quote/{ticker}/financials/")
    handle_cookies(driver)

    current_url = driver.current_url
    try:
        # check if page found
        if 'lookup' in current_url:
            print(f"Ticker {ticker} not found on Yahoo Finance. Skipping...")
            return None

        # Extract financial statement sections
        button = driver.find_element(By.CSS_SELECTOR, 
                             ".link2-btn.fin-size-x-small.rounded.svelte-122t2xs[data-ylk='elm:expand;sec:qsp-financials;slk:financials-report-all']")
        button.click()

        sections = driver.find_elements(By.CSS_SELECTOR, ".rowTitle")
        
        return [section.text for section in sections]

    except TimeoutException:
        print(f'Cookie consent overlay not found or already accepted at ticker,{ticker}')
        return None
    except NoSuchElementException:
        print(f"Failed to scrape,{ticker}")
        return None


def get_section_counts(tickers):
    section_counts = defaultdict(int)

    driver = get_driver(showGui=False)

    tickers_scraped = 0

    for ticker in tickers:
        sections = financial_data_points(driver, ticker)

        if sections:
            tickers_scraped += 1
            for section in sections:
                section_counts[section] += 1

        if tickers_scraped % 5 == 0:
            print(f"Scraped {tickers_scraped}...")

    driver.close()
    return section_counts, tickers_scraped


if __name__ == '__main__':
    tickers = get_tickers()

    section_counts, tickers_scraped = get_section_counts(tickers)

    print("Section,Count,Percentage")
    for section, count in section_counts.items():
              print(f"{section},{count},{str(round(count*100/tickers_scraped, 2))}%")

