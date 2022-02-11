# Copyright (c) --------- (see AUTHORS)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

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
