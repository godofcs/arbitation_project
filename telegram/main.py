import telebot
from telebot import types

ALL_MARKETS = ['Binance', 'ByBit', 'Okx', 'Huobi']
ALL_CURRENCY = ['RUB', 'USD', 'EUR', 'CNY', 'GBP']
ALL_BANKS = ['Raiffaizen', 'Sber', 'Tinkoff']

user_currency = ''
user_bank = ''
user_stock_markets = ['Binance', 'ByBit', 'Okx', 'Huobi']
user_limit = 0

bot = telebot.TeleBot('5630556319:AAHEgv_ykF1L5EADrJnzte6DTy9eyJg8nbE')


@bot.message_handler(commands=['start'])
def start(message):
    mess = 'Привет, Я бот созданный помогать....'
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       ['Help', 'Start Trading']))
    markup.add(*buttons)
    bot.send_message(message.chat.id, mess, reply_markup=markup)

    bot.register_next_step_handler(message, currency)


def currency(message):
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       ['Start Over', 'Help', 'RUB', 'USD', 'EUR', 'CNY', 'GBP']))
    markup.add(*buttons)
    mess = 'Choose the currency you will trade'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, limit)


def limit(message):
    global user_currency
    if message.text in ALL_CURRENCY:
        user_currency = message.text
    else:
        bot.send_message(message.chat.id, "I can't understand you shorty)")
        currency(message)

    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       ['Start Over', 'Help']))
    markup.add(*buttons)
    mess = 'Enter the limit (1000 RUB min)'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, stock_markets)


def stock_markets_buttons(el):
    if el in user_stock_markets:
        el = "✅ " + el
    return types.KeyboardButton(el)


def stock_markets(message):
    global user_limit
    if message.text is not "None":
        user_limit = message.text

    markup = types.ReplyKeyboardMarkup()

    buttons = list(map(lambda el: stock_markets_buttons(el),
                       ['Start Over', 'Help', 'Binance', 'ByBit', 'Okx', 'Huobi', 'Done']))
    markup.add(*buttons)
    mess = 'Except/Add stock markets you want to trade in'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, pre_stock_markets)


def pre_stock_markets(message):
    if message.text.strip() == "Done":
        bank(message)
    else:
        global user_stock_markets
        if message.text[0] == "✅":
            bot.send_message(message.chat.id, f"Removed {message.text[2:]} stock market")
            user_stock_markets.remove(message.text[2:])
        elif message.text in ALL_MARKETS:
            bot.send_message(message.chat.id, f"Add {message.text} stock market")
            user_stock_markets.append(message.text)
        else:
            bot.send_message(message.chat.id, "I can't understand you shorty)")
        message.text = "None"
        stock_markets(message)


def bank(message):
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       ['Start Over', 'Help', 'Sber', 'Tinkoff', 'Raiffaizen']))
    markup.add(*buttons)
    mess = 'Where do you hold your paper'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(message, answer)


def answer(message):
    global user_bank
    if message.text in ALL_BANKS:
        user_bank = message.text
    else:
        bot.send_message(message.chat.id, "I can't understand you shorty)")
        bank(message)
    print(user_bank, user_limit, user_currency, user_stock_markets)
    # Здесь вызываем парсер.
    # Здесь передаем данные из парсера в васин софт
    # Здесь отдаем данные клиенту.


bot.polling(none_stop=True)
