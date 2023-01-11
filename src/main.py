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
        all_offers = get_offers.get_offers(["RUB"], ["BTC", "ETH", "USDT", "BUSD", "BNB"], [2],
                                       ["binance", "bybit", "huobi"], ["Tinkoff", "Sberbank", "Raiffeisenbank"])
        message = "ТО ЧТО ОТПРАВЛЕТЕ В БОТА ОБРАТНО"

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

    for one_limit_id in all_offers:
        print(f"Это связки для следующих значений лимита: {one_limit_id[0]}")
        for offers in one_limit_id[1:]:
            print(counter.Counter(offers))
