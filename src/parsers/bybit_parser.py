from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import logging


def get_name(el):
    name = el.find_element(By.CLASS_NAME, "advertiser-name")
    return name.text


def get_col_orders(el):
    col_el = el.find_element(By.CLASS_NAME, "advertiser-info")
    col = col_el.find_element(By.CSS_SELECTOR, "span")
    return int(col.text.split()[0])


def get_complete_percent(el):
    percent = el.find_element(By.CLASS_NAME, "execute-rate")
    percent_str = percent.text
    return float(percent_str.split("%")[0])


def get_price(el):
    price = el.find_element(By.CLASS_NAME, "price-amount")
    txt = price.text
    return float("".join(txt.split(",")))


def get_limit(el):
    limit = el.find_elements(By.CLASS_NAME, "ql-value")
    mas_lim = []
    for el in limit[1].text.split("~"):
        lim = el.split()[0]
        lim = "".join(lim.split(","))
        mas_lim += [float(lim)]
    return mas_lim


def get_available(el):
    price = el.find_elements(By.CLASS_NAME, "ql-value")
    txt = price[0].text.split()[0]
    return float("".join(txt.split(",")))


def get_glass_position(driver):
    pos = []
    pos_element = driver.find_elements(By.XPATH, "//table/tbody/tr")
    kol = min(7, len(pos_element))
    for element in pos_element[:kol]:
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
            logging.debug("Append necessary position || bybit")
        except Exception as err:
            logging.warning("Necessary position do not append in glass || bybit")
    return pos


def parse(link, limit):
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    path = "geckodriver.exe"
    option = Options()
    option.headless = True
    logging.debug("Start browser || bybit")
    driver = Firefox(executable_path=path, options=option)
    driver.get(link)
    driver.set_window_size(1920, 1080)
    logging.debug("Successfully start browser || bybit")
    kol = 0
    while kol < 10:
        try:
            sleep(1)
            pre_buttons = driver.find_element(By.CLASS_NAME, "by-dialog__head")
            buttons = pre_buttons.find_elements(By.CSS_SELECTOR, "span")
            for button in buttons:
                button.click()
            logging.debug("Click necessary button || bybit")
            break
        except Exception as err:
            logging.warning("There is no necessary button || bybit")
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
            logging.debug("Click second necessary button || bybit")
            break
        except Exception as err:
            logging.warning("There is no second necessary button || bybit")
        kol += 1
    kol = 0
    while kol < 5:
        sleep(1)
        try:
            button = driver.find_element(By.CLASS_NAME, "by-dialog__btn")
            button.click()
            logging.debug("Click third necessary button || bybit")
            break
        except Exception as err:
            logging.warning("There is no third necessary button || bybit")
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
                logging.debug("Send key || bybit")
                break
        except Exception as err:
            logging.warning("Do not send key || bybit")
        kol += 1
    kol = 0
    while kol < 10:
        sleep(1)
        try:
            element = driver.find_elements(By.XPATH, "//table/tbody/tr")
            if len(element) > 1:
                logging.debug("Get necessary position || bybit")
                break
        except Exception as err:
            logging.warning("There is no necessary position || bybit")
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos


#if __name__ == "__main__":
#    print(parse("https://www.bybit.com/fiat/trade/otc/?actionType=0&token=BTC&fiat=RUB&paymentMethod=64", 10000))


