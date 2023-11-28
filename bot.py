import os
import telebot
from dotenv import load_dotenv
from telebot import types
from libgen_api import LibgenSearch
from icecream import ic
from helper_functions import Records
from random import choice

load_dotenv()

API_TOKEN = os.getenv('API_KEY')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands= ["start"])
def start_book_bot(message):
    gifs = ["https://media.giphy.com/media/Vbtc9VG51NtzT1Qnv1/giphy.gif","https://media.giphy.com/media/xTiIzJSKB4l7xTouE8/giphy.gif","https://media.giphy.com/media/mW05nwEyXLP0Y/giphy.gif"]
    bot.send_animation(message.chat.id, choice(gifs), caption= "Hello there, Broke ass nigga.\n I shall bestow upon you, Knowledge.🤯")
    button1 = types.BotCommand(command="start", description="Start the Bot")
    button2 = types.BotCommand(command="search", description="Name of book to be queried")
    button3 = types.BotCommand(command="help", description="Click for help")
    bot.set_my_commands([button1, button2, button3])
    bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands("commands"))

@bot.message_handler(commands=["help"])
def help_book_bot(message):
    help_gif = "https://media.giphy.com/media/1zjON7WqVVeKwlIGbT/giphy.gif"
    bot.send_animation(message.chat.id, help_gif, caption="Nothing to see here. Help yourself." )

@bot.message_handler(commands=['search'])
def search_book_bot(message):
    query_lst = message.text.split()
    query_lst = query_lst[1:]
    query = " ".join(query_lst)
    search = Records(query)
    search.get_records()
    bot.reply_to(message, "Here are the results")
    markup = types.InlineKeyboardMarkup(row_width=1)
    download_buttons = [
        types.InlineKeyboardButton("GET", url=search.download_links["GET"]),
        types.InlineKeyboardButton("Cloudflare", url=search.download_links["Cloudflare"]),
        types.InlineKeyboardButton("IPFS", url=search.download_links["IPFS.io"])
    ]
    next_button = types.InlineKeyboardButton("Next ⏩", callback_data="Next")
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data="Back")
    markup.add(*download_buttons)
    markup.add(back_button, next_button, row_width=2)
    bot.send_message(message.chat.id, search.reply, reply_markup=markup)
    
bot.infinity_polling()