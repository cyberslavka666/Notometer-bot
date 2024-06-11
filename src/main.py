import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Read tokens from files
with open("../res/TOKEN.txt") as file:
    TELEGRAM_TOKEN = file.readline().strip()

with open("../res/MY-API.txt") as file:
    COINMARKETCAP_API_KEY = file.readline().strip()

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_coin_price(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    if data['status']['error_code'] == 0:
        price = data['data'][symbol]['quote']['USD']['price']
        return f"The current price of {symbol} is ${price:.6f}"
    else:
        return f"Error fetching the price of {symbol}."


def get_notcoin_price():
    return get_coin_price('NOT')


def get_shitcoin_price():
    return get_coin_price('SHIT')


def get_durev_price():
    return get_coin_price('DUREV')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    price_button = KeyboardButton('/price')
    help_button = KeyboardButton('/help')
    markup.add(price_button, help_button)
    bot.send_message(message.chat.id, "👋 Hi! Use the buttons below to get the current price of NOTCOIN or for help. also don't forget to subscribe to the bot developer.", reply_markup=markup)


@bot.message_handler(commands=['price'])
def send_price(message):
    price_message = get_notcoin_price()
    markup = InlineKeyboardMarkup()
    shitcoin_button = InlineKeyboardButton(text="Get SHITCOIN Price", callback_data="get_shitcoin_price")
    durev_button = InlineKeyboardButton(text="Get DUREV Price", callback_data="get_durev_price")
    markup.add(shitcoin_button, durev_button)
    bot.send_message(message.chat.id, price_message, reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = "This bot provides cryptocurrency prices. Use /price to get the current price of NOTCOIN. Click the respective buttons to get prices for SHITCOIN or POVEL DUREV COIN, you also can write in support: @Notometer_support_bot."
    bot.send_message(message.chat.id, help_message)


@bot.callback_query_handler(func=lambda call: call.data == "get_shitcoin_price")
def send_shitcoin_price(call):
    price_message = get_shitcoin_price()
    bot.send_message(call.message.chat.id, price_message)


@bot.callback_query_handler(func=lambda call: call.data == "get_durev_price")
def send_durev_price(call):
    price_message = get_durev_price()
    bot.send_message(call.message.chat.id, price_message)


if __name__ == '__main__':
    bot.polling()
