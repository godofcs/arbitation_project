from src.parsers import parse_argument as pa
from src import get_offers as go
from src import counter
from src.db_requests import db_session

db_session.global_init("C:/Users/4739409/PycharmProjects/arbitation_project/bd/base.sqlite")

if __name__ == "__main__":
    # limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()
    all_offers = go.get_offers(["RUB"], ["BTC", "ETH", "USDT", "BUSD", "BNB", "SHIB"], [2], ["binance", "bybit", "huobi"],
                        ["Tinkoff", "Sberbank", "Raiffeisenbank"])
    for offer in all_offers:
        for el in offer:
            print("id: ", el.id, " market: ", el.market, " payment: ", el.payment, " sell_buy: ", el.sell_buy,
                  " init_coin: ", el.init_coin, " receive_coin: ", el.receive_coin, " id_limit: ", el.id_limit,
                  " price: ", el.price, "maker_commission: ", el.maker_commission,
                  " taker_commission ", el.taker_commission, " last_time_update: ", el.last_time_update)
        print("-------------------------------------------------------------------------------------------------------")
    #print(ans)
    #print(counter.Counter(ans))
