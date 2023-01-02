from data.binance_parser import parse as binance_parse
from data.bybit_parser import parse as bybit_parse
from data.analyse import analyse_glass
import datetime
from data import parse_argument as pa
from data import counter
from pyvirtualdisplay import Display


if __name__ == "__main__":
    #limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()
    ans = pa.parse_argument(1, ["RUB"], ["binance", "bybit", "huobi"], ["BTC", "USDT", "ETH"], ["Tinkoff"])



