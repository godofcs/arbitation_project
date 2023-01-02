from data.parsers.binance_parser import parse as binance_parse
from data.parsers.bybit_parser import parse as bybit_parse
from data.analyse import analyse_glass
import datetime
from data.db_requests import db_session, offers

db_session.global_init("C:/Users/4739409/PycharmProjects/arbitation_project/bd/base.sqlite")

all_crypto = {"USDT": {"binance": "USDT", "bybit": "USDT", "okx": "usdt"},
              "BTC": {"binance": "BTC", "bybit": "BTC", "okx": "btc"},
              "BUSD": {"binance": "BUSD", "bybit": "-", "okx": "-"},
              "BNB": {"binance": "BNB", "bybit": "-", "okx": "-"},
              "ETH": {"binance": "ETH", "bybit": "ETH", "okx": "eth"},
              "SHIB": {"binance": "SHIB", "bybit": "-", "okx": "-"}}
all_payment = {"Tinkoff": {"binance": "TinkoffNew", "bybit": "75"},
               "Sberbank": {"binance": "RosBankNew", "bybit": "185"},
               "Raiffeisenbank": {"binance": "RaiffeisenBank", "bybit": "64"},
               }  # "QIWI", "YandexMoneyNew"
all_fiat = {"RUB": {"binance": "RUB", "bybit": "RUB", "okx": "rub"}}
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
    "okx":
        {
            "buy": ["https://www.okx.cab/ru/p2p-markets/", "key=fiat", "/buy-", "key=crypto"],
            "sell": ["https://www.okx.cab/ru/p2p-markets/", "key=fiat", "/sell-", "key=crypto"]
        }
}

limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000, 7: 500000, 8: 1000000}
def get_limit(limit_id):
    return limits[limit_id]


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
                        mas_links.append([link, [market, fiat, crypto, payment, sell_buy]])

    print(len(mas_links))
    for i in mas_links[:4]:
        print(i)
    return mas_links


if __name__ == "__main__":
    big_dict = {}
    limit_id = 1
    limit = get_limit(limit_id)
    mas_links = make_mas_links(all_fiat.keys(), all_market.keys(), all_crypto.keys(), all_payment.keys())
    for link in mas_links[:4]:
        if "binance" in link[0]:
            glass = binance_parse(link[0], limit)
            new_offer = [analyse_glass(glass)] + link[1] + [datetime.datetime.now()]
            sessions = db_session.create_session()
            offer = sessions.query(offers.Offer).filter(offers.Offer.market == new_offer[1],
                                                        offers.Offer.init_coin == new_offer[2],
                                                        offers.Offer.receive_coin == new_offer[3],
                                                        offers.Offer.id_limit == limit_id).first()
            if offer is None:
                offer = offers.Offer()
                offer.market = new_offer[1]
                offer.init_coin = new_offer[2]
                offer.receive_coin = new_offer[3]
                offer.id_limit = limit_id
            offer.price = new_offer[0]
            offer.las_time_update = new_offer[-1]
            offer.taker_commission = 0.0
            offer.maker_commission = 0.1
            sessions.merge(offer)
            sessions.commit()
            sessions.close()
        elif "bybit" in link[0]:
            glass = bybit_parse(link[0], limit)
            new_offer = [analyse_glass(glass)] + link[1] + [datetime.datetime.now()]
            sessions = db_session.create_session()
            offer = sessions.query(offers.Offer).filter(offers.Offer.market == new_offer[1],
                                                        offers.Offer.init_coin == new_offer[2],
                                                        offers.Offer.receive_coin == new_offer[3],
                                                        offers.Offer.id_limit == limit_id).first()
            if offer is None:
                offer = offers.Offer()
                offer.market = new_offer[1]
                offer.init_coin = new_offer[2]
                offer.receive_coin = new_offer[3]
                offer.id_limit = limit_id
            offer.price = new_offer[0]
            offer.las_time_update = new_offer[-1]
            offer.taker_commission = 0.0
            offer.maker_commission = 0.0
            sessions.merge(offer)
            sessions.commit()
            sessions.close()

    sessions = db_session.create_session()
    offers = sessions.query(offers.Offer)
    for offer in offers:
        print(offer.market, offer.init_coin, offer.receive_coin, offer.id_limit, offer.price, offer.maker_commission, offer.taker_commission, offer.las_time_update)

