import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from environs import Env
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint


def parse_quotes(url, driver):
    quotes_list = [["Имя", "Цена"]]
    quotes_name = driver.find_elements(by=By.CLASS_NAME, value="symbol-word-break")
    quotes = [quote.text for quote in quotes_name]
    final_prices = driver.find_elements(
        by=By.XPATH, value="//td[@class='bold text-right']"
    )
    prices = [(price.text).replace(",", "") for price in final_prices]
    for element, value in enumerate(quotes):
        quote = [value, prices[element]]
        quotes_list.append(quote)
    return quotes_list


def click_to_market(base_url, driver):
    wait = WebDriverWait(driver, randint(3, 8))
    driver.get(base_url)
    wait.until(EC.url_to_be(base_url))

    market_data = driver.find_element(By.ID, "link_2")
    market_data.click()
    time.sleep(randint(4, 8))

    links = driver.find_elements(By.CLASS_NAME, "nav-link")
    for link in links:
        if link.text == "Pre-Open Market":
            link.click()
            time.sleep(randint(2, 4))
            market_url = driver.current_url
            break
    time.sleep(randint(4, 8))
    return market_url


def main():
    env = Env()
    env.read_env()
    driver_location = env("DRIVER_LOCATION")
    binary_location = env("BINARY_LOCATION")
    base_url = "https://www.nseindia.com/"

    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    service = Service(executable_path=driver_location)
    driver = webdriver.Chrome(service=service, options=options)

    market_url = click_to_market(base_url, driver)
    quotes = parse_quotes(market_url, driver)

    with open("quotes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(quotes)
        print("A CSV file named 'quotes.csv' created.")


if __name__ == "__main__":
    main()
