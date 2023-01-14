import sys
import json
sys.path.append("..")

from src import get_offers
from src import counter
from src.db_requests import db_session
import pika


def on_request(ch, method, props, body):
    args = json.loads(body.decode("utf-8"))
    response = run(args)
    ch.basic_publish(exchange="", routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run(requests_body):
    db_session.global_init()

    # [user_currency,user_limit,user_bank,user_stock_markets]
    user_currency = requests_body["user_currency"]
    user_limit = int(requests_body["user_limit"])
    user_bank = requests_body["user_bank"]
    user_stock = requests_body["user_stock_markets"]
    all_offers = get_offers.get_offers([user_currency], ["BTC", "USDT", "ETH", "BUSD", "BNB"],
                                       get_offers.get_limits_list(user_limit),
                                       user_stock, user_bank)
    message = ""
    for one_limit_id in all_offers:
        message = message + f"Это связки для следующих значений лимита: {one_limit_id[0]} \n"
        for offers in one_limit_id[1:]:
            message = message + counter.Counter(offers) + "\n"
        message = message + "\n"

    return message


if __name__ == "__main__":
    import time
    time.sleep(20)
    connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq:5672/%2F"))
    channel = connection.channel()

    channel.queue_declare(queue="rpc_queue")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)

    channel.start_consuming()
