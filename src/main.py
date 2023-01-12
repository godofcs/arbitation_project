import json

from src.parsers import parse_argument as pa
from src import get_offers
from src import counter
from src.db_requests import db_session

import pika
import traceback, sys

if __name__ == "__main__":
    db_session.global_init()

    # limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()

    connection_parameters = pika.ConnectionParameters('localhost', 5672)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue="from_bot_to_parser", durable=True)
    channel.queue_declare(queue="from_parser_to_bot")


    def callback(ch, method, properties, body):
        requests_body = json.loads(body)
        # [message.chat.id,user_currency,user_limit,user_bank,user_stock_markets]
        user_currency = requests_body[1]
        user_limit = requests_body[2]
        user_bank = requests_body[3]
        user_stock = requests_body[4]
        all_offers = get_offers.get_offers(user_currency, ["BTC", "USDT", "ETH", "BUSD", "BNB"], [2],
                                           user_stock, user_bank)
        message = "ТО ЧТО ОТПРАВЛЕТЕ В БОТА ОБРАТНО"

        for one_limit_id in all_offers:
            message = message + f"Это связки для следующих значений лимита: {one_limit_id[0]} \n"
            for offers in one_limit_id[1:]:
                message = message + counter.Counter(offers) + "\n"

        channel.basic_publish(exchange='',
                              routing_key='from_parser_to_bot',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))


    channel.basic_consume(callback, queue="from_bot_to_parser")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)

    channel.close()
