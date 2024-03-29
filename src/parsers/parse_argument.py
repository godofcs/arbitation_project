from parsers.binance_parser import parse as binance_parse
from parsers.bybit_parser import parse as bybit_parse
from analyse import analyse_glass
from parsers.huobi_parser import parse as huobi_parse
from db_requests import db_session
from db_requests.offers import Offer
from time import sleep
import logging


all_crypto = {"USDT": {"binance": "USDT", "bybit": "USDT", "huobi": "usdt"},
              "BTC": {"binance": "BTC", "bybit": "BTC", "huobi": "btc"},
              "BUSD": {"binance": "BUSD", "bybit": "-", "huobi": "-"},
              "BNB": {"binance": "BNB", "bybit": "-", "huobi": "-"},
              "ETH": {"binance": "ETH", "bybit": "ETH", "huobi": "eth"}}
all_payment = {"Tinkoff": {"binance": "TinkoffNew", "bybit": "75", "huobi": "Тинькофф"},
               "Sberbank": {"binance": "RosBankNew", "bybit": "185", "huobi": "Сбербанк"},
               "Raiffeisenbank": {"binance": "RaiffeisenBank", "bybit": "64", "huobi": "Райффайзенбанк"},
               }  # "QIWI", "YandexMoneyNew"
all_fiat = {"RUB": {"binance": "RUB", "bybit": "RUB", "huobi": "rub"}}
mas_sell_buy = ["sell", "buy"]
x = 1
all_market = {"binance":
    {
        "buy": ["https://p2p.binance.com/ru/trade/", "key=payment", "/", "key=crypto", "?fiat=", "key=fiat"],
        "sell": ["https://p2p.binance.com/ru/trade/sell/", "key=crypto", "?fiat=", "key=fiat", "&payment=",
                 "key=payment"]
    },
    "bybit":
        {
            "buy": ["https://www.bybit.com/fiat/trade/otc/?actionType=1&token=", "key=crypto", "&fiat=", "key=fiat",
                    "&paymentMethod=", "key=payment"],
            "sell": ["https://www.bybit.com/fiat/trade/otc/?actionType=0&token=", "key=crypto", "&fiat=", "key=fiat",
                     "&paymentMethod=", "key=payment"]
        },
    "huobi":
        {
            "buy": ["https://www.huobi.com/ru-ru/fiat-crypto/trade/buy-", "key=crypto", "-", "key=fiat", "/"],
            "sell": ["https://www.huobi.com/ru-ru/fiat-crypto/trade/sell-", "key=crypto", "-", "key=fiat", "/"]
        }
}

limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000, 7: 500000}

sell_buy = {"sell": 0, "buy": 1}


def get_limit(limit_id):  # Эта функция нужна для получения значения лимита по limit_id
    return limits[limit_id]


def get_sell_buy(type):  # Эта функция по типу действия: sell/buy возвращает его значение, как оно хранится в бд
    return sell_buy[type]


# Эта функция генерирует массив ссылок, с которыми мы работаем
def make_mas_links(cur_fiat, cur_market, cur_crypto, cur_payment):
    mas_links = []
    for sell_buy in mas_sell_buy:
        for payment in cur_payment:
            for fiat in cur_fiat:
                for crypto in cur_crypto:
                    for market in cur_market:
                        link = ""
                        flag = 0
                        for element in all_market[market][sell_buy]:
                            if "key=" in element:
                                key = element.split("=")[1]
                                if key == "payment":
                                    if all_payment[payment][market] == "-":
                                        flag = 1
                                        break
                                    link = link + all_payment[payment][market]
                                elif key == "crypto":
                                    if all_crypto[crypto][market] == "-":
                                        flag = 1
                                        break
                                    link = link + all_crypto[crypto][market]
                                elif key == "fiat":
                                    if all_fiat[fiat][market] == "-":
                                        flag = 1
                                        break
                                    link = link + all_fiat[fiat][market]
                            else:
                                link = link + element
                        if flag:
                            break
                        if sell_buy == "sell":
                            mas_links.append([link, [market, crypto, fiat, payment, sell_buy]])
                        else:
                            mas_links.append([link, [market, fiat, crypto, payment, sell_buy]])
    return mas_links


# Эта функция добавляет значение оффера в бд
def add_to_database(new_offer, limit_id, taker_commission, maker_commission, sessions):
#    sessions = db_session.create_session()
    offer = sessions.query(Offer).filter(Offer.market == new_offer[1],
                                         Offer.init_coin == new_offer[2],
                                         Offer.receive_coin == new_offer[3],
                                         Offer.payment == new_offer[4],
                                         Offer.sell_buy == get_sell_buy(new_offer[5]),
                                         Offer.id_limit == limit_id).first()
    if offer is None:
        offer = Offer()
        offer.market = new_offer[1]
        offer.init_coin = new_offer[2]
        offer.receive_coin = new_offer[3]
        offer.payment = new_offer[4]
        offer.sell_buy = get_sell_buy(new_offer[5])
        offer.id_limit = limit_id
    offer.price = new_offer[0]
    offer.taker_commission = taker_commission
    offer.maker_commission = maker_commission
    sessions.merge(offer)


# Эта функция отвечает за запуск парсеров
def parse_argument(limit_id, fiat_mas, market_mas, crypto_mas, payment_mas):
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    limit = get_limit(limit_id)
    mas_links = make_mas_links(fiat_mas, market_mas, crypto_mas, payment_mas)
    mas_add_to_data_base = []
    logging.debug("Generate links")
    k = 1
    for link in mas_links:
        if "binance" in link[0]:
            for i in range(5):
                try:
                    glass = binance_parse(link[0], limit)
                    new_offer = [analyse_glass(glass)] + link[1]
                    logging.debug(f"{k} binance {new_offer}")
                    if new_offer[5] == "buy":
                        mas_add_to_data_base.append([new_offer, limit_id, 0.0, 0.1])
                    else:
                        mas_add_to_data_base.append([new_offer, limit_id, 0.0, 100])
                    break
                except Exception as err:
                    logging.error(f"{err}")
                    logging.debug("Just, I am so tired on binance")
                    sleep(10)
        elif "bybit" in link[0]:
            for i in range(5):
                try:
                    glass = bybit_parse(link[0], limit)
                    new_offer = [analyse_glass(glass)] + link[1]
                    logging.debug(f"{k} bybit {new_offer}")
                    mas_add_to_data_base.append([new_offer, limit_id, 0.0, 0.0])
                    break
                except Exception as err:
                    logging.error(f"{err}")
                    logging.debug("Just, I am so tired on bybit")
                    sleep(10)
                    pass
        elif "huobi" in link[0]:
            for i in range(5):
                try:
                    glass = huobi_parse(link[0], limit, all_payment[link[1][3]]["huobi"])
                    new_offer = [analyse_glass(glass)] + link[1]
                    logging.debug(f"{k} huobi {new_offer}")
                    mas_add_to_data_base.append([new_offer, limit_id, 0.0, 0.0])
                    break
                except Exception as err:
                    logging.error(f"{err}")
                    logging.debug("Just, I am so tired on huobi")
                    sleep(10)
                    pass
        k += 1
    try:
        logging.debug("Start session")
        sessions = db_session.create_session()
        for el in mas_add_to_data_base:
            add_to_database(el[0], el[1], el[2], el[3], sessions)
        sessions.commit()
        sessions.close()
        logging.debug("End session")
    except Exception as err:
        logging.error(f"{err}")
        logging.warning("Session do not end successfully")

    # TODO сделать нормальный выбор по параметрам запросу

