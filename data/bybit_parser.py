from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from time import sleep


def get_name(el):
    name_el = el.find_element(By.CLASS_NAME, "css-1rhb69f")
    name = name_el.find_element(By.ID, "C2Cofferlistsell_link_merchant")
    return name.text


def get_col_orders(el):
    col_el = el.find_element(By.CLASS_NAME, "css-o358pi")
    col = col_el.find_element(By.CLASS_NAME, "css-1a0u4z7")
    return col.text


def get_complete_percent(el):
    col_el = el.find_element(By.CLASS_NAME, "css-o358pi")
    col = col_el.find_element(By.CLASS_NAME, "css-19crpgd")
    col_str = col.text
    return col_str.split("%")[0]


def get_price(el):
    price_el = el.find_element(By.CLASS_NAME, "css-11db165")
    price = price_el.find_element(By.CLASS_NAME, "css-1m1f8hn")
    return price.text


def get_limit(el):
    limit_el = el.find_element(By.CLASS_NAME, "css-lalzkr")
    pochti_limit = limit_el.find_element(By.CLASS_NAME, "css-16w8hmr")
    limit = pochti_limit.find_elements(By.CLASS_NAME, "css-4cffwv")
    mas_lim = []
    for el in limit:
        mas_lim.append(el.text)
    return mas_lim


def get_available(el):
    price_el = el.find_element(By.CLASS_NAME, "css-lalzkr")
    pochti_price = price_el.find_element(By.CLASS_NAME, "css-3v2ep2")
    price = pochti_price.find_element(By.CLASS_NAME, "css-vurnku")
    return price.text


def get_glass_position(driver):
    pos = []
    pos_element = driver.find_element(By.XPATH, "//table/tbody/tr")
    print(pos_element)
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
            print(buttons)
            for button in buttons:
                button.click()
                count += 1
            if count >= 4:
                break
        except Exception:
            pass
        kol += 1
        print()
    print(30)
    sleep(30)
    return
    pos = get_glass_position(driver)
    driver.close()
    return pos


if __name__ == "__main__":
    parse("https://www.bybit.com/fiat/trade/otc/?actionType=0&token=USDT&fiat=RUB&paymentMethod=75")

