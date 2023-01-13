import json

import pika
import traceback, sys
import json
import telebot
from telebot import types

from telegram.tele_bot.main import currency

API_KEY = "5630556319:AAHEgv_ykF1L5EADrJnzte6DTy9eyJg8nbE"

START_OVER_BUTTON = "НАЧАТЬ СНАЧАЛА"
HELP_BUTTON = "ПОМОЩЬ"
START_BUTTON = "НАЧАТЬ ТРЕЙДИТЬ"


bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    mess = 'Привет. Я бот, созданный для того, чтобы преумножить твой капитал с помощью сделок на криптовалютных ' \
           'биржах! Важно понимать, что за одну сделку ты не заработаешь на новый майбах, даже можешь и потерять свои ' \
           'деньги, но на дистанции ты точно заработаешь кругленькую сумму! Если тебе что-то не понятно или ты ' \
           'пользуешься нашим ботов впервые, то смело жми/пиши "Help". Желаю удачи! \n P.S Мы не являемся брокерами, ' \
           'не владеем инсайдерской информацией, наш бот пользуется открытой информации из интернета и предлагает ' \
           'вариант заработка. Мы не несем ответственность за ваши операции, вся информация несет только лишь ' \
           'рекомендательный характер '
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       [HELP_BUTTON, START_BUTTON]))
    markup.add(*buttons)
    bot.send_message(message.chat.id, mess, reply_markup=markup)

    bot.register_next_step_handler(message, currency)

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
        bot.register_next_step_handler(message, start)

    channel.basic_consume(callback, queue="from_parser_to_bot")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)

answer('')

