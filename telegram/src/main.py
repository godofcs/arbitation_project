import json

from src import get_offers
from src import counter
from src.db_requests import db_session

import pika
import traceback, sys


def run(requests_body):
    db_session.global_init()

    # [message.chat.id,user_currency,user_limit,user_bank,user_stock_markets]
    chat_id = requests_body[0]
    user_currency = requests_body[1]
    user_limit = requests_body[2]
    user_bank = requests_body[3]
    user_stock = requests_body[4]
    # TODO Протестировать работу get_limit_list
    print(chat_id)
    print(user_currency)
    print(user_limit)
    print(user_bank)
    print(user_stock)
    print(get_offers.get_limits_list(user_limit))
    all_offers = get_offers.get_offers([user_currency], ["BTC", "USDT", "ETH", "BUSD", "BNB"],
                                       get_offers.get_limits_list(user_limit),
                                       user_stock, user_bank)
    # ТО ЧТО ОТПРАВЛЕТЕ В БОТА ОБРАТНО
    message = ""
    print(11111111111111111111)
    print(len(all_offers))
    for one_limit_id in all_offers:
        message = message + f"Это связки для следующих значений лимита: {one_limit_id[0]} \n"
        for offers in one_limit_id[1:]:
            message = message + counter.Counter(offers) + "\n"
        message = message + "\n"

    print(message)

    return [chat_id, message]
