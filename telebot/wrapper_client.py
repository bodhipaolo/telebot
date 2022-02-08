import re
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


def w(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello World!")

def btc_reply(update: Update, context: CallbackContext):
    result = re.search('bitcoin', update.message.text)
    if result != None:
        message_reply = "Sei interessato a servizi Bitcoin"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message_reply)

#### MAIN 

updater = Updater(token='5197893187:AAHu9nLtenZcCC9PQ_uWM05yvMd3OvJyA7w', use_context=True)
dispatcher = updater.dispatcher

# Reply to /hello
hello_handler = CommandHandler('hello', hello)
dispatcher.add_handler(hello_handler)

# A message handler that replies in case the message contains bitcoin word
btc_handler = MessageHandler(Filters.text & (~Filters.command), btc_reply)
dispatcher.add_handler(btc_handler)

updater.start_polling()
