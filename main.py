from data.binance_parser import parse as binance_parse
from data.bybit_parser import parse as bybit_parse
from pyvirtualdisplay import Display

all_crypto = {"USDT": {"binance": "USDT", "bybit": "USDT"},
              "BTC": {"binance": "BTC", "bybit": "BTC"},
              "BUSD": {"binance": "BUSD", "bybit": "-"},
              "BNB": {"binance": "BNB", "bybit": "-"},
              "ETH": {"binance": "ETH", "bybit": "ETH"},
              "SHIB": {"binance": "SHIB", "bybit": "-"}}
all_payment = {"Tinkoff": {"binance": "TinkoffNew", "bybit": "75"},
               "Sberbank": {"binance": "RosBankNew", "bybit": "185"},
               "Raiffeisenbank": {"binance": "RaiffeisenBank", "bybit": "64"},
               }  # "QIWI", "YandexMoneyNew"
all_fiat = {"RUB": {"binance": "RUB", "bybit": "RUB"}}
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
        }
}
mas_links = []
for sell_buy in mas_sell_buy:
    for payment in all_payment.keys():
        for fiat in all_fiat.keys():
            for crypto in all_crypto.keys():
                for market in all_market.keys():  # Плохо, переделать
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
                    mas_links.append(link)

print(len(mas_links))
for i in mas_links[:4]:
    print(i)

big_dict = {}
limit = 1000

if __name__ == "__main__":
    for link in mas_links[:4]:
        if "binance" in link:
            big_dict[link] = binance_parse(link, limit)
        elif "bybit" in link:
            big_dict[link] = bybit_parse(link, limit)

    for i in big_dict.keys():
        print(big_dict[i])
