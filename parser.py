import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from selenium.webdriver.common.action_chains import ActionChains


def parse_quotes(url, driver):
    actions = ActionChains(driver)
    actions.scroll_by_amount(0, 50).perform()
    time.sleep(randint(2, 4))
    quotes_list = [["Имя", "Цена"]]

    quotes_name = driver.find_elements(By.CLASS_NAME, value="symbol-word-break")
    quotes = [quote.text for quote in quotes_name]
    final_prices = driver.find_elements(
        By.CSS_SELECTOR,
        value="tbody tr:nth-child(n) td:nth-child(7)",
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


def imitate_user(base_url, driver):
    wait = WebDriverWait(driver, randint(5, 11))
    driver.get(base_url)
    wait.until(EC.url_to_be(base_url))
    equity_market = driver.find_element(
        By.CSS_SELECTOR,
        value="div.col-md-2:nth-child(4) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)",
    )

    time.sleep(randint(1, 2))
    actions = ActionChains(driver)
    actions.scroll_to_element(equity_market).scroll_by_amount(0, 200).perform()
    time.sleep(randint(4, 8))
    actions.move_to_element(equity_market).click().perform()
    time.sleep(randint(4, 8))


def main():
    base_url = "https://www.nseindia.com/"
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)

    market_url = click_to_market(base_url, driver)
    quotes = parse_quotes(market_url, driver)

    with open("quotes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(quotes)
        print("A CSV file named 'quotes.csv' created.")

    imitate_user(base_url, driver)
    driver.quit()


if __name__ == "__main__":
    main()
