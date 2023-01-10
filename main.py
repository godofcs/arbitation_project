from src.parsers import parse_argument as pa
from src import counter


import pika
import sys, traceback
#не забудь добавить когда будешь копипастить код

if __name__ == "__main__":
    #limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()

    connection_parameters = pika.ConnectionParameters('localhost', 5672)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue="from_bot_to_parser")

    def callback(ch, method, properties, body):
        print(body)

    channel.basic_consume(callback, queue="from_bot_to_parser")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)


    # ans = pa.parse_argument(1, ["RUB"], ["binance", "bybit", "huobi"], ["BTC", "USDT", "ETH"], ["Tinkoff"])



