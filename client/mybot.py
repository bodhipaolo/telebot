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

import sys
import time

sys.path.append(".")

import botlog
from telebot import Telebot
from ui      import Buttons

bot         = Telebot("5197893187:AAHu9nLtenZcCC9PQ_uWM05yvMd3OvJyA7w")
bot.about   = "Working in progress of Telegram-Bot wrapped"
bot.owner   = "@bodhipaolo"

logger = botlog.get_logger(__name__)

# Command
@bot.command("ciao")
def ciao_command(chat, message, args):
    logger.debug("ciao_command called")

    logger.info("Printed immediately.")
    delay = 20
    time.sleep(delay)
    logger.info("Printed after %d seconds." % delay)
    chat.send("Ciao! Sono mybot")
    if message is not None:
        logger.info("message %s" % message.text)
    logger.info("args %s" % args)

# Message matches
@bot.message_matches(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
def email_set(chat, message, matches):
    logger.debug("email_set called")
    chat.send("Email sent to %s" % message.text)
    if message is not None:
        logger.info("message %s" % message.text)
    logger.info("matches %s" % matches)

# Message
@bot.message()
def message_detection(chat, message):
    logger.debug("Generic message")
    chat.send("This '%s' is your message" % message.text)
    if message is not None:
        logger.info("message %s" % message.text)

# Commands with buttons
@bot.command("direct")
def direct_command(chat, message, args):
    btns = Buttons()
    btns[0].callback("First button", "first", "")
    btns[0].callback("Secondary button", "second", "")
    btns[1].callback("Third button", "third", "")
    btns[2].callback("Fourth button", "fourth", "")
    if message is not None:
        logger.info("message %s" % message.text)
    logger.info("args %s" % args)
    chat.send("some message", attach=btns, syntax="markdown")

# Callback
@bot.callback("first")
def first_callback(query, data, chat, message):
    logger.debug("Enter first")
    chat.send("Your choice is %s" % data)
    if message is not None:
        logger.info("message %s" % message.text)
    logger.debug("Exit first")

# Callback
@bot.callback("third")
def third_callback(query, data, chat, message):
    logger.debug("Enter third")
    chat.send("Your choice is %s" % data)
    if message is not None:
        logger.info("message %s" % message.text)
    logger.debug("Exit third")

if __name__ == "__main__":
    bot.run()
