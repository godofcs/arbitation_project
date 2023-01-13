import telebot
from telebot import types
import pika
import json

API_KEY = "5630556319:AAHEgv_ykF1L5EADrJnzte6DTy9eyJg8nbE"

ALL_MARKETS = ['Binance', 'ByBit', 'Huobi']
ALL_CURRENCY = ['RUB', 'USD', 'EUR', 'CNY', 'GBP']
ALL_BANKS = ['Raiffeisenbank', 'Sberbank', 'Tinkoff"']

START_OVER_BUTTON = "НАЧАТЬ СНАЧАЛА"
START_BUTTON = "НАЧАТЬ ТРЕЙДИТЬ"
HELP_BUTTON = "ПОМОЩЬ"
INVALID_STRING = "Я тебя не понимаю :-("

RETURN = "Вернуться назад"
DONE = "Выполнено"

LEFT_BORDER = 1000
RIGHT_BORDER = 100000

user_currency = ''
user_bank = ALL_BANKS.copy()
user_stock_markets = ALL_MARKETS.copy()
user_limit = 0

bot = telebot.TeleBot(API_KEY)


def user_clear():
    global user_limit
    user_limit = 0
    global user_currency
    user_currency = ''
    global user_bank
    user_bank = ALL_BANKS.copy()
    global user_stock_markets
    user_stock_markets = ALL_MARKETS.copy()

@bot.message_handler(commands=['help'])
def help(message):
    helping_message = "Привет! Для начала взаимодействия с нашим ботом ты должен выбрать валюту(пока доступны " \
                      "операции только с рублем), банки и биржи, на которых ты будешь торговать. Запомни: чем больше " \
                      "выбранных банков и бирж, тем больше выгодных вариантов. Бот примерно будет работать 15-30 " \
                      "минут, пока завари себе кофе и подготовь печенюшки, скоро мы будем делать бабки! \n " \
                      "Энциклопедия терминов: Sell/Buy - в какой вкладке P2P следует совершать сделку; Maker/Taker - " \
                      "указывает на то в качестве кого стоит совершать сделку. Maker - сделку стоит совершать в " \
                      "качестве продавца, т.е вы назначаете цену(рекомендованную цену тебе покажет бот), Taker - вы " \
                      "пользуетесь уже имеющимся предложениями, просто переходите по объявлению и обмениваетесь " \
                      "монетами. \n Если что-то сломалось или тебе что-то не понятно, то пиши @vazy1 за помощью. " \
                      "version 0.0.1 "
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton(START_BUTTON)
    markup.add(button)
    bot.send_message(message.chat.id, helping_message, reply_markup=markup)
    bot.register_next_step_handler(message, currency)


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


def currency(message):
    if message.text.strip() == HELP_BUTTON:
        help(message)
        return
    elif message.text.strip() != START_BUTTON:
        bot.send_message(message.chat.id, INVALID_STRING)
        start(message)
        return
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       [HELP_BUTTON, START_OVER_BUTTON] + ALL_CURRENCY))
    markup.add(*buttons)
    mess = 'Выбери валюту для торговли'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, limit)


def limit(message):
    global user_currency
    if message.text.strip() in ALL_CURRENCY:
        user_currency = message.text.strip()
    elif message.text.strip() == HELP_BUTTON:
        user_clear()
        help(message)
        return
    elif message.text.strip() == START_OVER_BUTTON:
        user_clear()
        message.text = START_BUTTON
        currency(message)
        return
    else:
        message.text = START_BUTTON
        user_clear()
        bot.send_message(message.chat.id, INVALID_STRING)
        currency(message)
        return

    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       [HELP_BUTTON, START_OVER_BUTTON]))
    markup.add(*buttons)
    mess = 'Введи свою ставку (1000 RUB минимум)' # TO DO Если будем делать для многих валют, то тут надо
    # TO DO параметризовть лимит для разных валют
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, stock_markets)


def stock_markets_buttons(el):
    global user_stock_markets
    if el in user_stock_markets:
        el = "✅ " + el
    return types.KeyboardButton(el)


def stock_markets(message):
    global user_limit
    if message.text.strip() != RETURN:
        if message.text == START_OVER_BUTTON:
            user_clear()
            message.text = START_BUTTON
            currency(message)
            return
        elif message.text.strip() == HELP_BUTTON:
            user_clear()
            help(message)
            return

        int_limit = 0
        try:
            int_limit = int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, "Введите число пожалуйста")
            message.text = user_currency
            limit(message)
            return

        if not (LEFT_BORDER <= int_limit <= RIGHT_BORDER):
            bot.send_message(message.chat.id, f"Пожалуйста, введите ограничение на границы: min = {LEFT_BORDER}, "
                                              f"max = {RIGHT_BORDER}")
            message.text = user_currency
            limit(message)
            return
        user_limit = int_limit

    markup = types.ReplyKeyboardMarkup()

    buttons = list(map(lambda el: stock_markets_buttons(el),
                       [START_OVER_BUTTON, HELP_BUTTON] + ALL_MARKETS + [DONE]))
    markup.add(*buttons)
    mess = 'Выбери биржи на которых хочешь торговать!'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, pre_stock_markets)


def pre_stock_markets(message):
    if message.text.strip() == START_OVER_BUTTON:
        user_clear()
        message.text = START_BUTTON
        currency(message)
        return
    elif message.text.strip() == HELP_BUTTON:
        user_clear()
        help(message)
        return
    elif message.text.strip() == DONE:
        bank(message)
        return
    else:
        global user_stock_markets
        if message.text[2:].strip() in ALL_MARKETS:
            bot.send_message(message.chat.id, f"Удалить {message.text.strip()[2:]} биржу")
            user_stock_markets.remove(message.text.strip()[2:])
        elif message.text.strip() in ALL_MARKETS:
            bot.send_message(message.chat.id, f"Добавить {message.text.strip()} биржу")
            user_stock_markets.append(message.text.strip())
        else:
            bot.send_message(message.chat.id, INVALID_STRING)
        message.text = RETURN
        stock_markets(message)


def bank_button(el):
    global user_bank
    if el in user_bank:
        el = "✅ " + el
    return types.KeyboardButton(el)


def bank(message):
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: bank_button(el),
                       [START_OVER_BUTTON, HELP_BUTTON] + ALL_BANKS + [DONE]))
    markup.add(*buttons)
    mess = 'Где вы держите свои деньги?'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, pre_bank)


def pre_bank(message):
    if message.text.strip() == START_OVER_BUTTON:
        user_clear()
        message.text = START_BUTTON
        currency(message)
        return
    elif message.text.strip() == HELP_BUTTON:
        user_clear()
        help(message)
        return
    elif message.text.strip() == DONE:
        pre_answer(message)
        return
    else:
        global user_bank
        if message.text[2:].strip() in ALL_BANKS:
            bot.send_message(message.chat.id, f"Удалить {message.text[2:].strip()} банк")
            user_bank.remove(message.text[2:])
        elif message.text.strip() in ALL_BANKS:
            bot.send_message(message.chat.id, f"Добавить {message.text} банк")
            user_bank.append(message.text)
        else:
            bot.send_message(message.chat.id, INVALID_STRING)
        message.text = RETURN
        bank(message)


def pre_answer(message):
    global user_bank
    if message.text.strip() == START_OVER_BUTTON:
        user_clear()
        message.text = START_BUTTON
        currency(message)
        return
    elif message.text.strip() == HELP_BUTTON:
        user_clear()
        help(message)
        return
    elif message.text.strip() == DONE:
        connection_params = pika.ConnectionParameters('localhost', 5672)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        channel.queue_declare(queue="from_bot_to_parser", durable=True)
        channel.basic_publish(exchange='',
                              routing_key='from_bot_to_parser',
                              body=json.dumps([message.chat.id,
                                               user_currency,
                                               user_limit,
                                               user_bank,
                                               user_stock_markets]),
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))
        markup = types.ReplyKeyboardMarkup()
        buttons = [START_OVER_BUTTON, HELP_BUTTON]
        markup.add(*buttons)
        mess = 'Работаем...'
        bot.send_message(message.chat.id, mess, reply_markup=markup)
        connection.close()
    else:
        bot.send_message(message.chat.id, INVALID_STRING)
        bank(message)
        return

bot.polling(none_stop=True)
