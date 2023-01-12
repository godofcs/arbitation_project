from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep


def get_name(el):
    name = el.find_element(By.CLASS_NAME, "font14")
    #print(name.text)
    return name.text


def get_col_orders(el):
    col = el.find_element(By.CLASS_NAME, "grey-label-half")
    #print(int(col.text.split(":")[1].split("|")[0]))
    return int(col.text.split(":")[1].split("|")[0])


def get_complete_percent(el):
    percent = el.find_element(By.CLASS_NAME, "grey-label-half")
    percent_str = percent.text.split(":")[1].split("|")[0]
    #print(float(percent_str.split("%")[0]))
    return float(percent_str.split("%")[0])


def get_price(el):
    price = el.find_element(By.CLASS_NAME, "price")
    price = price.find_element(By.CSS_SELECTOR, "div")
    txt = price.text.split()[0]
    #print(1, txt)
    #print(float("".join(txt.split(","))))
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
    #print(mas_lim)
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
    #print("".join(txt.split(",")))
    return float("".join(txt.split(",")))


def get_glass_position(driver):
    pos = []
    #table = driver.find_element(By.CLASS_NAME, "trade-list__content")
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
        except Exception:
            print(Exception)
            pass
    return pos


def parse(link, limit, cur_payment):
    path = "geckodriver.exe"
    option = Options()
    option.headless = True
    driver = Firefox(executable_path=path, options=option)
    driver.get(link)
    # Это на всякий случай
    kol = 0
    while kol < 30:
        sleep(1)
        try:
            print(kol, "huobi try")
            button = driver.find_element(By.CLASS_NAME, "video-close")
            if button:
                button.click()
                print("huobi cool")
                break
        except Exception:
            pass
        kol += 1
    kol = 0
    while kol < 30:
        sleep(1)
        try:
            print(kol, "huobi seecond try")
            payment = driver.find_element(By.CLASS_NAME, "search-amount-container")
            if payment:
                input_place = payment.find_element(By.CLASS_NAME, "ivu-input")
                input_place.send_keys(f"{limit}")
                button = payment.find_element(By.CLASS_NAME, "submit-in")
                button.click()
                print("huobi second cool")
                break
        except Exception:
            pass
        kol += 1
    kol = 0
    while kol < 30:
        sleep(1)
        try:
            print("huobi last try")
            pre = driver.find_elements(By.CLASS_NAME, "pay-search-container")[2]
            if pre:
                print(1)
                pre.click()
                pre_input = driver.find_element(By.CLASS_NAME, "pay-method-haveHistory")
                input = pre_input.find_element(By.CLASS_NAME, "ivu-input-default")
                input.send_keys(f"{cur_payment}")
                print(2)
                sleep(0.5)
                but = pre_input.find_element(By.CLASS_NAME, 'cursor')
                but.click()
                print(3)
                sleep(0.5)
                but = pre_input.find_element(By.CLASS_NAME, 'multiSelect-payments-confirm')
                but.click()
                print(4)
                break
        except Exception:
            pass
        kol += 1
    kol = 0
    while kol < 30:
        sleep(1)
        try:
            print("last attempt")
            element = driver.find_elements(By.CLASS_NAME, "otc-trade-list")
            if len(element) > 1:
                print(len(element))
                break
        except Exception:
            pass
        kol += 1
    pos = get_glass_position(driver)
    driver.close()
    return pos


#if __name__ == "__main__":
#    print(parse("https://www.huobi.com/ru-ru/fiat-crypto/trade/buy-eth-rub/", 10000, "Тинькофф"))


