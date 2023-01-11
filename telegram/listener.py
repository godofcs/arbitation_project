import json

import pika
import traceback, sys
import json
import telebot
from telebot import types

API_KEY = "5630556319:AAHEgv_ykF1L5EADrJnzte6DTy9eyJg8nbE"

START_OVER_BUTTON = "НАЧАТЬ СНАЧАЛА"
HELP_BUTTON = "ПОМОЩЬ"

bot = telebot.TeleBot(API_KEY)

def answer(message):
    connection_params = pika.ConnectionParameters('localhost', 5672)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    markup = types.ReplyKeyboardMarkup()
    buttons = [START_OVER_BUTTON, HELP_BUTTON]
    markup.add(*buttons)
    def callback(ch, method, properties, body):
        request = json.loads(body)
        bot.send_message(body[0], body[1], reply_markup=markup)

    channel.basic_consume(callback, queue="from_parser_to_bot")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)

answer('')

