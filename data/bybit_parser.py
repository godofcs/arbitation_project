from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from time import sleep


def get_name(el):
    name = el.find_element(By.CLASS_NAME, "advertiser-name")
    print(name.text)
    return name.text


def get_col_orders(el):
    col_el = el.find_element(By.CLASS_NAME, "advertiser-info")
    col = col_el.find_element(By.CSS_SELECTOR, "span")
    print(col.text)
    return col.text


def get_complete_percent(el):
    col_el = el.find_element(By.CLASS_NAME, "by-popover__el")
    col = col_el.find_element(By.CSS_SELECTOR, "span")
    col_str = col.text
    print(col_str)
    return col_str.split("%")[0]


def get_price(el):
    price = el.find_element(By.CLASS_NAME, "price-amount")
    print(price.text)
    return price.text


def get_limit(el):
    limit = el.find_elements(By.CLASS_NAME, "ql-value")
    mas_lim = []
    for el in limit[1].text.split("~"):
        mas_lim += [el]
    print(mas_lim)
    return mas_lim


def get_available(el):
    price = el.find_elements(By.CLASS_NAME, "ql-value")
    print(price[0].text)
    return price[0].text


def get_glass_position(driver):
    pos = []
    #table = driver.find_element(By.CLASS_NAME, "trade-list__content")
    pos_element = driver.find_elements(By.XPATH, "//table/tbody/tr")
    for element in pos_element[:7]:
        print(element)
        try:
            data = {
                "name": get_name(element),
                "col_orders": get_col_orders(element),
                "complete_percent": get_complete_percent(element),
                "price": get_price(element),
                "limit": get_limit(element),
                "available": get_available(element)
            }
            pos += [data]
        except Exception:
            pass
    return pos


def parse(link):
    driver = Chrome(executable_path="./chromedriver.exe")
    driver.get("https://www.bybit.com/fiat/trade/otc/?actionType=0&token=USDT&fiat=RUB&paymentMethod=75")
    kol = 0
    count = 0
    while kol < 30:
        sleep(1)
        try:
            pre_buttons = driver.find_element(By.CLASS_NAME, "by-dialog__head")
            buttons = pre_buttons.find_elements(By.CSS_SELECTOR, "span")
            for button in buttons:
                button.click()
                count += 1
            if count >= 4:
                break
        except Exception:
            pass
        kol += 1
    kol = 0
    while kol < 30:
        sleep(1)
        try:
            table = driver.find_element(By.CLASS_NAME, "trade-list__content")
            element = table.find_elements(By.XPATH, "//table/tbody/tr")
            print(len(element))
            if len(element) > 7:
                break
        except Exception:
            pass
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos


if __name__ == "__main__":
    print(parse("https://www.bybit.com/fiat/trade/otc/?actionType=0&token=USDT&fiat=RUB&paymentMethod=75"))

