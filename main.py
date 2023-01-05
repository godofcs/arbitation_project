from src.parsers import parse_argument as pa
from src import counter

# TODO в хелп добавить подсказку про комиссию за перевод.

if __name__ == "__main__":
    #limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()
    ans = pa.parse_argument(1, ["RUB"], ["binance", "bybit", "huobi"], ["BTC", "USDT", "ETH"], ["Tinkoff"])



