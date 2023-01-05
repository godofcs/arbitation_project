from src.parsers import parse_argument as pa
from datetime import datetime

limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000, 7: 500000, 8: 1000000}

if __name__ == "__main__":
    for limit_id in limits.keys():
        pa.parse_argument(limit_id, ["RUB"], ["binance", "bybit", "huobi"],
                          ["BTC", "USDT", "ETH", "BUSD", "BNB", "SHIB"], ["Tinkoff", "Sberbank", "Raiffeisenbank"])
