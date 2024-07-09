from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome driver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the Yahoo Finance page for AAPL
driver.get("https://finance.yahoo.com/quote/AAPL/")

# Wait for the page to load completely
wait = WebDriverWait(driver, 10)

try:
    # Example: Extract the stock price
    stock_price_element = driver.find_elements(By.TAG_NAME, "li")
    # Print the results
    print(stock_price_element)

finally:
    # Close the driver
    driver.quit()

