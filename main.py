from src.parsers import parse_argument as pa
from src import get_offers as go
from src import counter
from src.db_requests import db_session

db_session.global_init("C:/Users/4739409/PycharmProjects/arbitation_project/bd/base.sqlite")

if __name__ == "__main__":
    # limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()
    all_offers = go.get_offers(["RUB"], ["BTC", "ETH", "USDT", "BUSD", "BNB", "SHIB"], [2], ["binance", "bybit", "huobi"],
                        ["Tinkoff", "Sberbank", "Raiffeisenbank"])
    for offers in all_offers:
        print(counter.Counter(offers))
