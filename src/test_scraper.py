from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import TimeoutException


def handle_cookies(driver):
    try:
        # Wait up to 3 seconds for the consent modal to show up
        consent_overlay = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.consent-overlay')))

        # Click the "Accept all" button
        accept_all_button = consent_overlay.find_element(By.CSS_SELECTOR, '.accept-all')
        accept_all_button.click()
        print('Cookies handles')
    except TimeoutException:
        print('Cookie consent overlay not found or already accepted')

def scrape_summary(driver, ticker):
    driver.get(f"https://finance.yahoo.com/quote/{ticker}")
    handle_cookies(driver)

    try:
        # Example: Extract the stock price
        stock_price_element = driver.find_element(By.CSS_SELECTOR, 'h1.svelte-3a2v0c')

        # Print the results
        print(stock_price_element.text)

        # Wait until the 'Financials' link is present
        financials_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/quote/AAPL/financials/"]')
    
        # Click the 'Financials' link
        financials_link.click()

    except TimeoutException:
        print('Cookie consent overlay not found or already accepted')


def scrape_financials(driver, ticker):
    driver.get("https://finance.yahoo.com/quote/AAPL/financials/")
    try:
        # Example: Extract the stock price
        stock_price_element = driver.find_element(By.CSS_SELECTOR, 'h1.svelte-3a2v0c')

        # Print the results
        print(stock_price_element.text)

        # Wait until the 'Financials' link is present
        financials_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/quote/AAPL/financials/"]')
    
        # Click the 'Financials' link
        financials_link.click()

    except TimeoutException:
        print('Cookie consent overlay not found or already accepted')



if __name__ == '__main__':
    # Set up Chrome options
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(2)

    ticker = 'AAPL'

    scrape_summary(driver, ticker)
    scrape_financials(driver, ticker)

    driver.close()

