from data.binance_parser import parse
from pyvirtualdisplay import Display

mas_crypto = ["USDT", "BTC", "BUSD", "BNB", "ETH", "SHIB"]
mas_payment = ["TinkoffNew", "RosBankNew", "RaiffeisenBank"]    # "QIWI", "YandexMoneyNew"
mas_fiat = ["RUB"]
mas_sell_buy = ["sell", "buy"]
mas_market = ["https://p2p.binance.com/ru/trade/"]
mas_links = []
for market in mas_market:
    for sell_buy in mas_sell_buy:
        for fiat in mas_fiat:
             for payment in mas_payment:
                for crypto in mas_crypto:
                    mas_links += [market + sell_buy + "/" + crypto + "?fiat=" + fiat + "&payment=" + payment]
big_dict = {}

if __name__ == "__main__":
    for link in mas_links:
        big_dict[link] = parse(link)

    for i in big_dict.keys():
        print(big_dict[i])


