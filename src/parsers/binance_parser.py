from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import logging


def get_name(el):
    name_el = el.find_element(By.CLASS_NAME, "css-1rhb69f")
    name = name_el.find_element(By.ID, "C2Cofferlistsell_link_merchant")
    return name.text


def get_col_orders(el):
    col_el = el.find_element(By.CLASS_NAME, "css-o358pi")
    col = col_el.find_element(By.CLASS_NAME, "css-1a0u4z7")
    return int(col.text.split()[0])


def get_complete_percent(el):
    col_el = el.find_element(By.CLASS_NAME, "css-o358pi")
    col = col_el.find_element(By.CLASS_NAME, "css-19crpgd")
    col_str = col.text
    return float(col_str.split("%")[0])


def get_price(el):
    price_el = el.find_element(By.CLASS_NAME, "css-11db165")
    price = price_el.find_element(By.CLASS_NAME, "css-1m1f8hn")
    txt = price.text
    return float("".join(txt.split(",")))


def get_limit(el):
    limit_el = el.find_element(By.CLASS_NAME, "css-lalzkr")
    pochti_limit = limit_el.find_element(By.CLASS_NAME, "css-16w8hmr")
    limit = pochti_limit.find_elements(By.CLASS_NAME, "css-4cffwv")
    mas_lim = []
    for el in limit:
        lim = el.text.split("\n")[1]
        lim = "".join(lim.split(","))
        mas_lim.append(float(lim))
    return mas_lim


def get_available(el):
    price_el = el.find_element(By.CLASS_NAME, "css-lalzkr")
    pochti_price = price_el.find_element(By.CLASS_NAME, "css-3v2ep2")
    price = pochti_price.find_element(By.CLASS_NAME, "css-vurnku")
    txt = price.text.split()[0]
    return float("".join(txt.split(",")))


def get_glass_position(driver):
    pos = []
    element = driver.find_element(By.CLASS_NAME, "css-1mf6m87")
    pos_element = element.find_elements(By.CLASS_NAME, "css-ovjtyv")
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
            pos.append(data)
            logging.debug("Append necessary position || binance")
        except Exception as err:
            logging.warning("Necessary position do not append in glass || binance")
    return pos


def parse(link, limit):
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    path = "geckodriver.exe"
    option = Options()
    option.headless = True
    logging.debug("Start browser || binance")
    driver = Firefox(executable_path=path, options=option)
    driver.set_window_size(1920, 1080)
    driver.get(link)
    logging.debug("Successfully start browser || binance")
    kol = 0
    while kol < 10:
        sleep(1)
        try:
            input_place = driver.find_element(By.ID, "C2Csearchamount_searchbox_amount")
            button = driver.find_element(By.ID, "C2Csearchamount_btn_search")
            #button2 = driver.find_element(By.CLASS_NAME, "css-1pcqseb")
            if input_place and button:  # and button2:
                #button2.click()
                input_place.click()
                input_place.send_keys(f"{limit}")
                button.click()
                logging.debug("Send key || binance")
                break
        except Exception as err:
            logging.warning("Do not send key || binance")
        kol += 1
    kol = 0
    while kol < 10:
        sleep(1)
        try:
            element = driver.find_element(By.CLASS_NAME, "css-1mf6m87")
            pos_element = element.find_elements(By.CLASS_NAME, "css-ovjtyv")
            if len(pos_element) > 1:
                logging.debug("Get necessary position || binance")
                break
        except Exception as err:
            logging.warning("There is no necessary position || binance")
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos


#if __name__ == "__main__":
#    print(parse("https://p2p.binance.com/ru/trade/sell/USDT?fiat=RUB&payment=TinkoffNew", 1000))