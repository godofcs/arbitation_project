from src.parsers.binance_parser import parse as binance_parse
from src.parsers.bybit_parser import parse as bybit_parse
from src.analyse import analyse_glass
from src.parsers.huobi_parser import parse as huobi_parse
import datetime
from src.db_requests import db_session
from src.db_requests.offers import Offer
from pyvirtualdisplay import Display

db_session.global_init("C:/Users/4739409/PycharmProjects/arbitation_project/bd/base.sqlite")

all_crypto = {"USDT": {"binance": "USDT", "bybit": "USDT", "huobi": "usdt"},
              "BTC": {"binance": "BTC", "bybit": "BTC", "huobi": "btc"},
              "BUSD": {"binance": "BUSD", "bybit": "-", "huobi": "-"},
              "BNB": {"binance": "BNB", "bybit": "-", "huobi": "-"},
              "ETH": {"binance": "ETH", "bybit": "ETH", "huobi": "eth"},
              "SHIB": {"binance": "SHIB", "bybit": "-", "huobi": "-"}}
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

limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000, 7: 500000, 8: 1000000}

sell_buy = {"sell": 0, "buy": 1}


def get_limit(limit_id):
    return limits[limit_id]


def get_sell_buy(type):
    return sell_buy[type]


def make_mas_links(cur_fiat, cur_market, cur_crypto, cur_payment):
    mas_links = []
    for sell_buy in mas_sell_buy:
        for payment in cur_payment:
            for fiat in cur_fiat:
                for crypto in cur_crypto:
                    for market in cur_market:  # Плохо, переделать
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
    print(len(mas_links))
    for i in mas_links:
        print(i)
    return mas_links


def add_to_database(new_offer, limit_id, taker_commission, maker_commission):
    sessions = db_session.create_session()
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
    offer.last_time_update = new_offer[-1]
    offer.taker_commission = taker_commission
    offer.maker_commission = maker_commission
    sessions.merge(offer)
    sessions.commit()
    sessions.close()


def actual_date(last_date):
    now = datetime.datetime.now()
    return (now - last_date).seconds < 100000001800  # 1800


def checking_the_relevance_of_information(mas_links, limit_id):
    sessions = db_session.create_session()
    new_mas_links = []
    for link in mas_links:
        args = link[1]
        offer = sessions.query(Offer).filter(Offer.market == args[0],
                                             Offer.init_coin == args[1],
                                             Offer.receive_coin == args[2],
                                             Offer.payment == args[3],
                                             Offer.sell_buy == get_sell_buy(args[4]),
                                             Offer.id_limit == limit_id
                                             ).first()
        if offer is None:
            new_mas_links.append(link)
            continue
        if not actual_date(offer.last_time_update):
            new_mas_links.append(link)
    sessions.close()
    return new_mas_links


def parse_argument(limit_id, fiat_mas, market_mas, crypto_mas, payment_mas):
    limit = get_limit(limit_id)
    mas_links = make_mas_links(fiat_mas, market_mas, crypto_mas, payment_mas)
    mas_links = checking_the_relevance_of_information(mas_links, limit_id)
    for link in mas_links:
        if "binance" in link[0]:
            glass = binance_parse(link[0], limit)
            new_offer = [analyse_glass(glass)] + link[1] + [datetime.datetime.now()]
            print("binance", new_offer)
            if new_offer[5] == "buy":
                add_to_database(new_offer, limit_id, 0.0, 100)
            else:
                add_to_database(new_offer, limit_id, 100, 0.1)
        elif "bybit" in link[0]:
            glass = bybit_parse(link[0], limit)
            new_offer = [analyse_glass(glass)] + link[1] + [datetime.datetime.now()]
            print("bybit", new_offer)
            add_to_database(new_offer, limit_id, 0.0, 0.0)
        elif "huobi" in link[0]:
            glass = huobi_parse(link[0], limit, all_payment[link[1][3]]["huobi"])
            new_offer = [analyse_glass(glass)] + link[1] + [datetime.datetime.now()]
            print("huobi", new_offer)
            add_to_database(new_offer, limit_id, 0.0, 0.0)
    # TODO сделать нормальный выбор по параметрам запросу
    sessions = db_session.create_session()
    offers = sessions.query(Offer)
    ans = []
    for offer in offers:
        ans.append(offer)
        #ans += [[offer.market, offer.init_coin, offer.receive_coin, offer.id_limit, offer.price, offer.maker_commission,
        #         offer.taker_commission, offer.last_time_update]]
    return ans
