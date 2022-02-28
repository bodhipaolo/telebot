# Copyright (c) --------- (see AUTHORS)
#
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

from telegram       import Update
from telegram.ext   import Updater
from telegram.ext   import CallbackContext
from telegram.ext   import CommandHandler
from telegram.ext   import MessageHandler
from telegram.ext   import CallbackQueryHandler
from telegram.ext   import ChatMemberHandler
from telegram.ext   import Filters

from listeners      import CommandListener
from listeners      import MessageMatchListener
from listeners      import MessageContainsListener
from listeners      import CallbackListener
from listeners      import ChatMemberListener
from listeners      import InternalCommandListener
from consumers      import ConsumerManager

from internal_commands import show_chats_command
from internal_commands import start_command
import botlog       

logger = botlog.get_logger(__name__)

class Telebot:
    name            = 'Telebot: Telegram Bot Wrapper'
    owner           = 'NA'
    about           = 'A simple wrapper of python-telegram-bot library'
    _updater        = None
    _dispatcher     = None

    def __init__(self, api_key):
        self._updater           = Updater(token='5197893187:AAHu9nLtenZcCC9PQ_uWM05yvMd3OvJyA7w', use_context=True)
        self._dispatcher        = self._updater.dispatcher
        self._dispatcher.bot_data.setdefault("bot_ref", dict()))
        self._dispatcher.bot_data["bot_ref"]['name']   = self.name
        self._dispatcher.bot_data["bot_ref"]['owner']  = self.owner
        self._dispatcher.bot_data["bot_ref"]['about']  = self.about
        self.consumer_manager   = ConsumerManager()
        self.consumer_manager.initialize()

    def _init_handlers(self):
        self._chatmember_callback()
        self._internal_commands()

    def get_chatid(username):
        """ Return the chat id corresponding to the username parameter
        """
        return self._dispatcher.bot.bot_data

    def command(self, cmd_name):
        """It decorates Telegram-Bot user commands
        @param cmd_name is the name of command i.e.: "hello" for /hello
        """
        def inner(cmd_call):
            logger.debug('Enter inner of command decorator')
            listener    = CommandListener(cmd_name, cmd_call, self.consumer_manager)
            handler     = CommandHandler(cmd_name, listener.listener)
            disp_ret    = self._dispatcher.add_handler(handler)
            logger.debug('Exiting inner...')
            return cmd_call
        return inner

    def message_matches(self, regex):
        """It decorates Telegram-Bot message matches
        @param regex is a string repressenting the regular expression for message matching
        """
        def inner(msg_call):
            logger.debug('Enter inner of message_matches')
            listener    = MessageMatchListener(msg_call, regex, self.consumer_manager)
            handler     = MessageHandler(Filters.regex(regex) & (~Filters.command), listener.listener)
            #handler    = MessageHandler(Filters.text & (~Filters.command), task.listener) 
            disp_ret    = self._dispatcher.add_handler(handler) 
            return msg_call
        return inner

    def message_contains(self, token):
        """It decorates Telegram-Bot message 
        """
        def inner(msg_call):
            logger.debug('Enter inner of message_contains')
            listener    = MessageContainsListener(msg_call, token, self.consumer_manager)
            handler     = MessageHandler(Filters.text & (~Filters.command), listener.listener) 
            disp_ret    = self._dispatcher.add_handler(handler) 
            return msg_call
        return inner

    def callback(self, cmd_name):
        """It decorates Telegram-Bot user commands
        @param cmd_name is the name of command i.e.: "hello" for /hello
        """
        def inner(cmd_call):
            logger.debug('Enter inner of command decorator')
            listener    = CallbackListener(cmd_name, cmd_call, self.consumer_manager)
            handler     = CallbackQueryHandler(listener.listener, pattern = f"^{cmd_name}_*")
            disp_ret    = self._dispatcher.add_handler(handler)
            logger.debug('Exiting inner...')
            return cmd_call
        return inner

    def _chatmember_callback(self):
        # Handle members joining/leaving chats.
        # Handle members joining/leaving chats.
        logger.debug('Enter inner of command decorator')
        listener    = ChatMemberListener()
        handler     = ChatMemberHandler(listener.listener, ChatMemberHandler.ANY_CHAT_MEMBER)
        disp_ret    = self._dispatcher.add_handler(handler)

    def _internal_commands(self):
        # Register internal commands not exposed to client
        logger.debug('Enter _internal_commands')
        for call_name, callback in (("show_chats", show_chats_command), ("start", start_command)):
            listener    = InternalCommandListener(call_name, callback, self.consumer_manager)
            handler     = CommandHandler(call_name, listener.listener)
            disp_ret    = self._dispatcher.add_handler(handler)

    def run(self):
        """Enter event loop
        """
        logger.info ("initialize default handlers")
        self._init_handlers()
        logger.info("%s Launch consumer threads..." % (__name__))
        self.consumer_manager.start()
        logger.info("%s Enter event loop..." % (__name__))
        self._updater.start_polling()
        self._updater.idle()
        logger.info("%s Telegram-bot handlers removed." % (__name__))
        self.consumer_manager.stop()
        logger.info("%s All consumer threads stopped." % (__name__))





