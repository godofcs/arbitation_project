from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium_stealth import stealth
from time import sleep
import os


def get_name(el):
    name = el.find_element(By.CLASS_NAME, "advertiser-name")
    #print(name.text)
    return name.text


def get_col_orders(el):
    col_el = el.find_element(By.CLASS_NAME, "advertiser-info")
    col = col_el.find_element(By.CSS_SELECTOR, "span")
    #print(int(col.text.split()[0]))
    return int(col.text.split()[0])


def get_complete_percent(el):
    percent = el.find_element(By.CLASS_NAME, "execute-rate")
    percent_str = percent.text
    #print(float(percent_str.split("%")[0]))
    return float(percent_str.split("%")[0])


def get_price(el):
    price = el.find_element(By.CLASS_NAME, "price-amount")
    txt = price.text
    #print(1, txt)
    #print(float("".join(txt.split(","))))
    return float("".join(txt.split(",")))


def get_limit(el):
    limit = el.find_elements(By.CLASS_NAME, "ql-value")
    mas_lim = []
    for el in limit[1].text.split("~"):
        lim = el.split()[0]
        lim = "".join(lim.split(","))
        mas_lim += [float(lim)]
    #print(mas_lim)
    return mas_lim


def get_available(el):
    price = el.find_elements(By.CLASS_NAME, "ql-value")
    txt = price[0].text.split()[0]
    #print("".join(txt.split(",")))
    return float("".join(txt.split(",")))


def get_glass_position(driver):
    pos = []
    #table = driver.find_element(By.CLASS_NAME, "trade-list__content")
    pos_element = driver.find_elements(By.XPATH, "//table/tbody/tr")
    kol = min(7, len(pos_element))
    for element in pos_element[:kol]:
        #print(element)
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
            print(Exception)
            pass
    return pos


def parse(link, limit):
    path = "geckodriver.exe"
    option = Options()
    option.headless = True
    driver = Firefox(executable_path=path, options=option)
    driver.get(link)
    driver.set_window_size(1920, 1080)
    kol = 0
    while kol < 10:
        try:
            sleep(1)
            pre_buttons = driver.find_element(By.CLASS_NAME, "by-dialog__head")
            buttons = pre_buttons.find_elements(By.CSS_SELECTOR, "span")
            for button in buttons:
                button.click()
            break
        except Exception:
            pass
        kol += 1
    # Это на всякий случай
    kol = 0
    while kol < 2:
        sleep(1)
        try:
            pre_buttons = driver.find_element(By.CLASS_NAME, "otc-ad-close")
            buttons = pre_buttons.find_elements(By.CSS_SELECTOR, "i")
            for button in buttons:
                button.click()
            break
        except Exception:
            pass
        kol += 1
    kol = 0
    while kol < 5:
        sleep(1)
        try:
            button = driver.find_element(By.CLASS_NAME, "by-dialog__btn")
            button.click()
            break
        except Exception:
            pass
        kol += 1
    # До сюда
    kol = 0
    while kol < 10:
        sleep(1)
        try:
            input_place = driver.find_elements(By.CLASS_NAME, "by-input__inner")[1]
            if input_place:
                input_place.click()
                input_place.send_keys(f"{limit}")
                break
        except Exception:
            pass
        kol += 1
    kol = 0
    while kol < 10:
        sleep(1)
        try:
            element = driver.find_elements(By.XPATH, "//table/tbody/tr")
            if len(element) > 1:
                break
        except Exception:
            pass
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos


#if __name__ == "__main__":
#    print(parse("https://www.bybit.com/fiat/trade/otc/?actionType=0&token=BTC&fiat=RUB&paymentMethod=64", 10000))


