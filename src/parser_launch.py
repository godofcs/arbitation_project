from parsers import parse_argument as pa
from db_requests import db_session
import threading
from time import sleep
import logging


limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000}


def run_parser():
    threads = [threading.Thread(target=foo, args=[i], daemon=True) for i in limits.keys()]
    for thread in threads:
        logging.debug("Thread start")
        thread.start()

    logging.debug("All thread start")

    for thread in threads:
        thread.join()
        logging.debug("Thread end")

    logging.debug("All thread end")


def foo(limit_id):
    pa.parse_argument(limit_id, ["RUB"], ["binance", "bybit", "huobi"],
                      ["BTC", "USDT", "ETH", "BUSD", "BNB"], ["Tinkoff", "Sberbank", "Raiffeisenbank"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    db_session.global_init()
    while True:
        logging.debug("Start parser")
        run_parser()
        sleep(600)
