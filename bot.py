import os
import telebot
from dotenv import load_dotenv
from telebot import types
from helper_functions import Records
from random import choice
import logging

load_dotenv()

"""
Setting environment variables
"""

API_TOKEN = os.getenv('API_KEY')
ADMIN_ID = os.getenv("ADMIN_ID")

"""
Configuring log files
"""

tg_logger = logging.getLogger('TeleBot')
tg_logger.setLevel(logging.WARNING)
tg_logger.propagate = False

logging.basicConfig(filename="status.log", level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


bot = telebot.TeleBot(API_TOKEN)
search = None
record_pool = {}

print('Bot Started')


@bot.message_handler(commands=["start"])
def start_book_bot(message):
    """
    Initializing menu commands
    """

    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    logging.info(
        f"{start_book_bot.__name__} | {user_name} | {user_id} has started the bot!")

    gifs = ["https://media.giphy.com/media/Vbtc9VG51NtzT1Qnv1/giphy.gif",
            "https://media.giphy.com/media/xTiIzJSKB4l7xTouE8/giphy.gif", "https://media.giphy.com/media/mW05nwEyXLP0Y/giphy.gif"]
    reply = f"Hello there @{user_name}, Broke ass nigga.\n I shall bestow upon you, Knowledge.🤯"
    bot.send_animation(message.chat.id, choice(gifs), caption=reply)

    button1 = types.BotCommand(command="start", description="Start the Bot")
    button2 = types.BotCommand(
        command="search", description="Name of book to be queried")
    button3 = types.BotCommand(command="help", description="Click for help")
    button4 = types.BotCommand(command="update", description="Update the bot")
    button5 = types.BotCommand(
        command="clear", description="clear the log file")
    bot.set_my_commands([button1, button2, button3, button4, button5])
    bot.set_chat_menu_button(
        message.chat.id, types.MenuButtonCommands("commands"))
    logging.info(
        f"{start_book_bot.__name__} | Menu Commands have been initialized.")


@bot.message_handler(commands=["help"])
def help_book_bot(message):
    help_gif = "https://media.giphy.com/media/1zjON7WqVVeKwlIGbT/giphy.gif"
    bot.send_animation(message.chat.id, help_gif,
                       caption="Nothing to see here. Help yourself.")


@bot.message_handler(commands=['search'])
def search_book_bot(message):
    """
    Get the records of the given query and display them along with download buttons and button to go to next record.
    Alert user if they did not enter a query.
    """
    global search
    global record_pool

    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    message_id = message.message_id

    query_lst = message.text.split()
    query_lst = query_lst[1:]
    query = " ".join(query_lst)

    if user_id not in record_pool:
        record_pool.update({f'{user_id}': []})

    if len(query) > 0:

        logging.info(f"{search_book_bot.__name__} | Querying {query}...")
        search = Records(query, record_pool)
        search.reset(user_id)
        search.initialize_records(user_id)

        reply = "_Please wait, results are being fetched_"
        bot.reply_to(message, reply, parse_mode='Markdown')

        reply_text, download_links, pointer = search.get_records(0, user_id)
        bot.edit_message_text(text=f"Here are the results. @{user_name}",
                              chat_id=chat_id,
                              message_id=message_id+1)

        markup = types.InlineKeyboardMarkup(row_width=1)
        download_buttons = [
            types.InlineKeyboardButton("GET", url=download_links["GET"]),
            types.InlineKeyboardButton(
                "Cloudflare", url=download_links["Cloudflare"]),
            types.InlineKeyboardButton("IPFS", url=download_links["IPFS.io"])
        ]
        next_button = types.InlineKeyboardButton(
            "Next ⏩", callback_data="Next")
        markup.add(*download_buttons, row_width=3)
        markup.add(next_button, row_width=1)
        logging.info(f"{search_book_bot.__name__} | {reply_text}")
        bot.send_message(message.chat.id, reply_text,
                         reply_markup=markup, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Enter a query!")

    @bot.callback_query_handler(func=lambda call: call.data == "Next")
    def next_btn(call):
        """
        Get next records if it exists else alert user that there are no more next records.
        """
        user_id = str(call.from_user.id)

        logging.info(f"{next_btn.__name__} | Getting next result..")
        reply_text, download_links, pointer = search.get_records(1, user_id)
        if download_links != None:
            markup = types.InlineKeyboardMarkup(row_width=1)
            download_buttons = [
                types.InlineKeyboardButton("GET", url=download_links["GET"]),
                types.InlineKeyboardButton(
                    "Cloudflare", url=download_links["Cloudflare"]),
                types.InlineKeyboardButton(
                    "IPFS", url=download_links["IPFS.io"])
            ]

            next_button = types.InlineKeyboardButton(
                "Next ⏩", callback_data="Next")
            back_button = types.InlineKeyboardButton(
                "Back 🔙", callback_data="Back")
            markup.add(*download_buttons, row_width=3)
            if pointer >= len(record_pool[user_id])-1:
                markup.add(back_button, row_width=1)
            else:
                markup.add(back_button, next_button, row_width=2)
            logging.info(f"{next_btn.__name__} | Got next result!")
            logging.info(f"{next_btn.__name__} | {reply_text}")
            bot.edit_message_text(text=reply_text, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=markup, parse_mode='Markdown')
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton(
                "Back 🔙", callback_data="Back")
            markup.add(back_button, row_width=1)
            logging.info(f"{next_btn.__name__} | {reply_text}")
            bot.edit_message_text(text=reply_text, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=markup, parse_mode='Markdown')

    @bot.callback_query_handler(func=lambda call: call.data == "Back")
    def back_btn(call):
        """
        Get previous record if it exists else alert user that there are no more previous records.
        """
        user_id = str(call.from_user.id)

        logging.info(f"{back_btn.__name__} | Getting previous result..")
        reply_text, download_links, pointer = search.get_records(-1, user_id)
        if download_links != None:
            markup = types.InlineKeyboardMarkup(row_width=1)
            download_buttons = [
                types.InlineKeyboardButton("GET", url=download_links["GET"]),
                types.InlineKeyboardButton(
                    "Cloudflare", url=download_links["Cloudflare"]),
                types.InlineKeyboardButton(
                    "IPFS", url=download_links["IPFS.io"])
            ]

            next_button = types.InlineKeyboardButton(
                "Next ⏩", callback_data="Next")
            back_button = types.InlineKeyboardButton(
                "Back 🔙", callback_data="Back")
            markup.add(*download_buttons, row_width=3)
            if pointer <= 0:
                markup.add(next_button, row_width=1)
            else:
                markup.add(back_button, next_button, row_width=2)
            logging.info(f"{back_btn.__name__} | Got previous result!")
            logging.info(reply_text)
            bot.edit_message_text(text=reply_text, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=markup, parse_mode='Markdown')
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            next_button = types.InlineKeyboardButton(
                "Next ⏩", callback_data="Next")
            markup.add(next_button, row_width=1)
            logging.info(f"{back_btn.__name__} | {reply_text}")
            bot.edit_message_text(text=reply_text, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['clear'])
def clear_logs(message):
    """
    Clears the log file
    """

    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        with open("status.log", "w"):
            pass
        logging.info(
            f"{clear_logs.__name__} | {user_name} | {user_id} cleared the logs.")
        reply = f"The log file has been cleared. @{user_name}"
        bot.reply_to(message, reply)
    else:
        logging.info(
            f"{clear_logs.__name__} | Log file clearing unsuccesful {user_name} | {user_id} not a ADMIN")
        clear_gif = "https://media.giphy.com/media/pUUcydt2WxjSXgYIoK/giphy.gif"
        bot.send_animation(message.chat.id, clear_gif,
                           caption="Come back when you are an ADMIN")


@bot.message_handler(commands=['update'])
def update(message):
    user_name = message.from_user.username
    user_id = str(message.from_user.id)
    reply = f"This feature is under construction.  @{user_name}🏗️🚧👷"
    bot.reply_to(message, reply)


bot.infinity_polling()
