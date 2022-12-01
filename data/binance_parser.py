from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
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
    element = driver.find_element(By.CLASS_NAME, "css-1mf6m87")
    pos_element = element.find_elements(By.CLASS_NAME, "css-ovjtyv")
    for element in pos_element[:7]:
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
        except Exception:
            pass
    return pos


def parse(link):
    driver = Chrome(executable_path="./chromedriver.exe")
    driver.get(link)
    kol = 0
    while kol < 30:
        sleep(1)
        try:
            element = driver.find_element(By.CLASS_NAME, "css-1mf6m87")
            pos_element = element.find_elements(By.CLASS_NAME, "css-ovjtyv")
            button = driver.find_element(By.CLASS_NAME, "css-1pcqseb")
            if button and len(pos_element) > 7:
                button.click()
                break
        except Exception:
            pass
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos

