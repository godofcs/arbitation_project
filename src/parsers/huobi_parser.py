from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import logging


def get_name(el):
    name = el.find_element(By.CLASS_NAME, "font14")
    return name.text


def get_col_orders(el):
    col = el.find_element(By.CLASS_NAME, "grey-label-half")
    return int(col.text.split(":")[1].split("|")[0])


def get_complete_percent(el):
    percent = el.find_element(By.CLASS_NAME, "grey-label-half")
    percent_str = percent.text.split(":")[1].split("|")[0]
    return float(percent_str.split("%")[0])


def get_price(el):
    price = el.find_element(By.CLASS_NAME, "price")
    price = price.find_element(By.CSS_SELECTOR, "div")
    txt = price.text.split()[0]
    return float("".join(txt.split(",")))


def get_limit(el):
    pre_limit = el.find_element(By.CLASS_NAME, "limit")
    limit = pre_limit.find_elements(By.CSS_SELECTOR, "span")
    lim1 = limit[0].text
    lim2 = limit[1].text
    lim2 = "".join(lim2.split(","))
    lim2 = lim2.split("-")[1]
    lim2_txt = lim2.split(".")[0] + "."
    for el in lim2.split(".")[1]:
        if el.isdigit():
            lim2_txt = lim2_txt + el
        else:
            break
    mas_lim = [float("".join(lim1.split(","))), float(lim2_txt)]
    return mas_lim


def get_available(el):
    price = el.find_element(By.CLASS_NAME, "stock")
    pre_txt = price.text
    txt = pre_txt.split(".")[0] + "."
    for el in pre_txt.split(".")[1]:
        if el.isdigit():
            txt = txt + el
        else:
            break
    # print("".join(txt.split(",")))
    return float("".join(txt.split(",")))


def get_glass_position(driver):
    pos = []
    # table = driver.find_element(By.CLASS_NAME, "trade-list__content")
    pos_element = driver.find_elements(By.CLASS_NAME, "otc-trade-list")
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
            logging.debug("Append necessary position || huobi")
        except Exception as err:
            logging.warning("Necessary position do not append in glass || huobi")
    return pos


def parse(link, limit, cur_payment):
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    path = "geckodriver.exe"
    option = Options()
    option.headless = True
    logging.debug("Start browser || huobi")
    driver = Firefox(executable_path=path, options=option)
    driver.set_window_size(1920, 1080)
    driver.get(link)
    logging.debug("Successfully start browser || bybit")
    # Это на всякий случай
    kol = 0
    while kol < 15:
        sleep(1)
        try:
            # тут возможно нужно другой класс поставить если работать не будет
            button = driver.find_element(By.CLASS_NAME, "close-box")
            if button:
                button.click()
                logging.debug("Click necessary button || huobi")
                break
        except Exception as err:
            logging.warning("There is no necessary button || huobi")
        kol += 1
    kol = 0
    while kol < 15:
        sleep(1)
        try:
            payment = driver.find_element(By.CLASS_NAME, "search-amount-container")
            if payment:
                input_place = payment.find_element(By.CLASS_NAME, "ivu-input")
                input_place.send_keys(f"{limit}")
                button = payment.find_element(By.CLASS_NAME, "submit-in")
                button.click()
                logging.debug("Send key || huobi")
                break
        except Exception as err:
            logging.warning("Do not send key || huobi")
        kol += 1
    kol = 0
    while kol < 15:
        sleep(1)
        try:
            pre = driver.find_elements(By.CLASS_NAME, "pay-search-container")[2]
            if pre:
                pre.click()
                pre_input = driver.find_element(By.CLASS_NAME, "pay-method-haveHistory")
                input = pre_input.find_element(By.CLASS_NAME, "ivu-input-default")
                input.send_keys(f"{cur_payment}")
                sleep(0.5)
                but = pre_input.find_element(By.CLASS_NAME, 'cursor')
                but.click()
                sleep(0.5)
                but = pre_input.find_element(By.CLASS_NAME, 'multiSelect-payments-confirm')
                but.click()
                logging.debug("Send second key || huobi")
                break
        except Exception as err:
            logging.warning("Do not send second key || huobi")
        kol += 1
    kol = 0
    while kol < 15:
        sleep(1)
        try:
            element = driver.find_elements(By.CLASS_NAME, "otc-trade-list")
            if len(element) > 1:
                logging.debug("Get necessary position || huobi")
                break
        except Exception as err:
            logging.warning("There is no necessary position || huobi")
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos

# if __name__ == "__main__":
#    print(parse("https://www.huobi.com/ru-ru/fiat-crypto/trade/buy-eth-rub/", 10000, "Тинькофф"))
