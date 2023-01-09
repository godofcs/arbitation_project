from src.parsers import parse_argument as pa
from src import get_offers
from src import counter
from src.db_requests import db_session

db_session.global_init("C:/Users/4739409/PycharmProjects/arbitation_project/bd/base.sqlite")

if __name__ == "__main__":
    # limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()
    all_offers = get_offers.get_offers(["RUB"], ["BTC", "ETH", "USDT", "BUSD", "BNB"], [2],
                                       ["binance", "bybit", "huobi"], ["Tinkoff", "Sberbank", "Raiffeisenbank"])
    for one_limit_id in all_offers:
        print(f"Это связки для следующих значений лимита: {one_limit_id[0]}")
        for offers in one_limit_id[1:]:
            print(counter.Counter(offers))
