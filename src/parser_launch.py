from src.parsers import parse_argument as pa
from src.db_requests import db_session
import schedule
import threading
from time import sleep
import time


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


db_session.global_init()

#schedule.every(10).seconds.do(job)

if __name__ == "__main__":
    #schedule.every(30).minutes.do(job)
    #schedule.every().minutes.do(job)
    while True:
        run_parser()
        sleep(600)
