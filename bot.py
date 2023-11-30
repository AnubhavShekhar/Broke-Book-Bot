import os
import telebot
from dotenv import load_dotenv
from telebot import types
from libgen_api import LibgenSearch
from icecream import ic
from helper_functions import Records
from random import choice
import logging

load_dotenv()

API_TOKEN = os.getenv('API_KEY')
ADMIN_ID = os.getenv("ADMIN_ID")

tg_logger = logging.getLogger('TeleBot')
tg_logger.setLevel(logging.WARNING)
tg_logger.propagate = False

logging.basicConfig(filename="status.log", level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands= ["start"])
def start_book_bot(message):
    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    logging.info(f"{user_name} | {user_id} has started the bot!")

    gifs = ["https://media.giphy.com/media/Vbtc9VG51NtzT1Qnv1/giphy.gif","https://media.giphy.com/media/xTiIzJSKB4l7xTouE8/giphy.gif","https://media.giphy.com/media/mW05nwEyXLP0Y/giphy.gif"]
    reply = f"Hello there @{user_name}, Broke ass nigga.\n I shall bestow upon you, Knowledge.🤯"
    bot.send_animation(message.chat.id, choice(gifs), caption=reply)

    button1 = types.BotCommand(command="start", description="Start the Bot")
    button2 = types.BotCommand(command="search", description="Name of book to be queried")
    button3 = types.BotCommand(command="help", description="Click for help")
    button4 = types.BotCommand(command="update", description="Update the bot")
    button5 = types.BotCommand(command="clear", description="clear the log file")
    bot.set_my_commands([button1, button2, button3, button4, button5])
    bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands("commands"))
    logging.info("Menu Commands have been initialized.")


@bot.message_handler(commands=["help"])
def help_book_bot(message):
    help_gif = "https://media.giphy.com/media/1zjON7WqVVeKwlIGbT/giphy.gif"
    bot.send_animation(message.chat.id, help_gif, caption="Nothing to see here. Help yourself." )

@bot.message_handler(commands=['search'])
def search_book_bot(message):
    user_name = message.from_user.username
    user_id = str(message.from_user.id)

    query_lst = message.text.split()
    query_lst = query_lst[1:]
    query = " ".join(query_lst)
    if len(query) > 0:
        logging.info(f"Querying {query}...")
        search = Records(query)
        search.reset()
        search.initialize_records()

        reply = f"Here are the results. @{user_name}"
        bot.reply_to(message, reply)

        reply_text, download_links = search.get_records(0)
        markup = types.InlineKeyboardMarkup(row_width=1)
        download_buttons = [
            types.InlineKeyboardButton("GET", url=download_links["GET"]),
            types.InlineKeyboardButton("Cloudflare", url=download_links["Cloudflare"]),
            types.InlineKeyboardButton("IPFS", url=download_links["IPFS.io"])
        ]
        next_button = types.InlineKeyboardButton("Next ⏩", callback_data="Next")
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data="Back")
        markup.add(*download_buttons)
        markup.add(back_button, next_button, row_width=2)
        logging.info(reply_text)
        bot.send_message(message.chat.id, reply_text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Enter a query!")

    @bot.callback_query_handler(func= lambda call: call.data == "Next")
    def next_button(call):
        logging.info("Getting next result..")
        reply_text, download_links = search.get_records(1)
        markup = types.InlineKeyboardMarkup(row_width=1)
        download_buttons = [
            types.InlineKeyboardButton("GET", url=download_links["GET"]),
            types.InlineKeyboardButton("Cloudflare", url=download_links["Cloudflare"]),
            types.InlineKeyboardButton("IPFS", url=download_links["IPFS.io"])
        ]
        next_button = types.InlineKeyboardButton("Next ⏩", callback_data="Next")
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data="Back")
        markup.add(*download_buttons)
        markup.add(back_button, next_button, row_width=2)
        logging.info("Got next result!")
        logging.info(reply_text)
        bot.edit_message_text(text=reply_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func= lambda call: call.data == "Back")
    def back_button(call):
        logging.info("Getting previous result..")
        reply_text, download_links = search.get_records(-1)
        markup = types.InlineKeyboardMarkup(row_width=1)
        download_buttons = [
            types.InlineKeyboardButton("GET", url=download_links["GET"]),
            types.InlineKeyboardButton("Cloudflare", url=download_links["Cloudflare"]),
            types.InlineKeyboardButton("IPFS", url=download_links["IPFS.io"])
        ]
        next_button = types.InlineKeyboardButton("Next ⏩", callback_data="Next")
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data="Back")
        markup.add(*download_buttons)
        markup.add(back_button, next_button, row_width=2)
        logging.info("Got previous result!")
        logging.info(reply_text)
        bot.edit_message_text(text=reply_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.message_handler(commands=['clear'])
def clear_logs(message):
    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        with open("status.log", "w"):
            pass
        logging.info(f"{user_name} | {user_id} cleared the logs.")
        reply = f"The log file has been cleared. @{user_name}"
        bot.reply_to(message, reply)
    else:
        logging.info(f"Log file clearing unsuccesful {user_name} | {user_id} not a ADMIN")
        clear_gif = "https://media.giphy.com/media/pUUcydt2WxjSXgYIoK/giphy.gif"
        bot.send_animation(message.chat.id, clear_gif, caption="Come back when you are an ADMIN" )

@bot.message_handler(commands=['update'])
def update(message):
    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    reply = f"This feature is under construction.  @{user_name}🏗️🚧👷"
    bot.reply_to(message, reply)

bot.infinity_polling()