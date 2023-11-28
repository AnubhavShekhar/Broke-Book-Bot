import os
import telebot
from dotenv import load_dotenv
from telebot import types
from libgen_api import LibgenSearch
from icecream import ic

load_dotenv()

API_TOKEN = os.getenv('API_KEY')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands= ["start"])
def start_book_bot(message):
    bot.reply_to(message, "Hello I am the broke mans book bot!")
    button1 = types.BotCommand(command="start", description="Start the Bot")
    button2 = types.BotCommand(command="search", description="Name of book to be queried")
    button3 = types.BotCommand(command="help", description="Click for help")
    bot.set_my_commands([button1, button2, button3])
    bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands("commands"))

@bot.message_handler(commands=["help"])
def help_book_bot(message):
    bot.reply_to(message, "Nothing to see here.. Help yourself ;)")

@bot.message_handler(commands=['search'])
def search_book_bot(message):
    query_lst = message.text.split()
    query_lst = query_lst[1:]
    query = " ".join(query_lst)
    s = LibgenSearch()
    results = s.search_title(query)
    filtered_search_results = []

    for result in results:
        download_links = s.resolve_download_links(result)
        formatting = f"""
Title: {result['Title']}\n
Author : {result['Author']}\n
Year: {result['Year']}\n
Extension: {result['Extension']}\n
Direct Download Links:\n
GET: {download_links["GET"]}\n
Cloudflare: {download_links['Cloudflare']}\n
IPFS: {download_links["IPFS.io"]}\n{"-"*20}
                    """
        filtered_search_results.append(formatting)
        if result == results[3]:
            break

    reply = "\n".join(filtered_search_results)
    bot.reply_to(message, "Here are the results")
    bot.send_message(message.chat.id, reply)

bot.polling()