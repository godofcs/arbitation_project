from parsers import parse_argument as pa
from db_requests import db_session
import threading
from time import sleep


limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000}


def run_parser():
    threads = [threading.Thread(target=foo, args=[i], daemon=True) for i in limits.keys()]
    for thread in threads:
        print("Thread start")
        thread.start()

    print("Start")

    for thread in threads:
        thread.join()
        print("Thread end")

    print("End")


def foo(limit_id):
    pa.parse_argument(limit_id, ["RUB"], ["binance", "bybit", "huobi"],
                      ["BTC", "USDT", "ETH", "BUSD", "BNB"], ["Tinkoff", "Sberbank", "Raiffeisenbank"])


if __name__ == "__main__":
    db_session.global_init()
    while True:
        run_parser()
        sleep(600)
