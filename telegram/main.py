import telebot
from telebot import types

API_KEY = "5630556319:AAHEgv_ykF1L5EADrJnzte6DTy9eyJg8nbE"

ALL_MARKETS = ['Binance', 'ByBit', 'Okx', 'Huobi']
ALL_CURRENCY = ['RUB', 'USD', 'EUR', 'CNY', 'GBP']
ALL_BANKS = ['Raiffaizen', 'Sber', 'Tinkoff']

START_OVER_BUTTON = "Start Over"
START_BUTTON = "Start Trading"
HELP_BUTTON = "Help"

RETURN = "fuckingshitbitchsukableat"
DONE = "Done"

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


def help(message):
    helping_message = "Message for help"
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton(START_BUTTON)
    markup.add(button)
    bot.send_message(message.chat.id, helping_message, reply_markup=markup)
    bot.register_next_step_handler(message, currency)


@bot.message_handler(commands=['start'])
def start(message):
    mess = 'Привет, Я бот созданный помогать....'
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
        bot.send_message(message.chat.id, "I can't understand you shorty)")
        start(message)
        return
    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       [HELP_BUTTON, START_OVER_BUTTON] + ALL_CURRENCY))
    markup.add(*buttons)
    mess = 'Choose the currency you will trade'
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
        bot.send_message(message.chat.id, "I can't understand you shorty)")
        currency(message)
        return

    markup = types.ReplyKeyboardMarkup()
    buttons = list(map(lambda el: types.KeyboardButton(el),
                       [HELP_BUTTON, START_OVER_BUTTON]))
    markup.add(*buttons)
    mess = 'Enter the limit (1000 RUB min)'
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
            bot.send_message(message.chat.id, "Please enter the limit which is number, not word")
            message.text = user_currency
            limit(message)
            return

        if not (LEFT_BORDER <= int_limit <= RIGHT_BORDER):
            bot.send_message(message.chat.id, f"Please enter the limit on borders: min = {LEFT_BORDER}, "
                                              f"max = {RIGHT_BORDER}")
            message.text = user_currency
            limit(message)
            return
        user_limit = int_limit

    markup = types.ReplyKeyboardMarkup()

    buttons = list(map(lambda el: stock_markets_buttons(el),
                       [START_OVER_BUTTON, HELP_BUTTON] + ALL_MARKETS + [DONE]))
    markup.add(*buttons)
    mess = 'Except/Add stock markets you want to trade in'
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
            bot.send_message(message.chat.id, f"Removed {message.text.strip()[2:]} stock market")
            user_stock_markets.remove(message.text.strip()[2:])
        elif message.text.strip() in ALL_MARKETS:
            bot.send_message(message.chat.id, f"Added {message.text.strip()} stock market")
            user_stock_markets.append(message.text.strip())
        else:
            bot.send_message(message.chat.id, "I can't understand you shorty)")
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
    mess = 'Where do you hold your paper'
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
        answer(message)
        return
    else:
        global user_bank
        if message.text[2:].strip() in ALL_BANKS:
            bot.send_message(message.chat.id, f"Removed {message.text[2:].strip()} bank")
            user_bank.remove(message.text[2:])
        elif message.text.strip() in ALL_BANKS:
            bot.send_message(message.chat.id, f"Added {message.text} bank")
            user_bank.append(message.text)
        else:
            bot.send_message(message.chat.id, "I can't understand you shorty)")
        message.text = RETURN
        bank(message)


def answer(message):
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
        bot.send_message(message.chat.id, "We are working...")
        print(user_bank, user_limit, user_currency, user_stock_markets)
    else:
        bot.send_message(message.chat.id, "I can't understand you shorty)")
        bank(message)
        return


bot.polling(none_stop=True)
