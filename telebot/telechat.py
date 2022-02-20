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

from telegram       import Chat
from telegram       import Update
from telegram       import InlineKeyboardButton
from telegram       import InlineKeyboardMarkup
from telegram.ext   import CallbackContext
from telegram.ext   import CommandHandler

import botlog

class Telechat:
    name        = 'Telegram Bot Chat class'
    _context   = None 
    _update    = None 

    def __init__(self, update, callback_context):
        """ it intiatiates an instance with the proper Telegram-Bot ojects
        @attr _context is for CallbackConext Telegram-Bot object
        @attr _update is for Update Telegram-Bot object
        """
        self._context   = callback_context
        self._update    = update
        self.logger     = botlog.get_logger(__name__)
    
    def get_chat_id(username):
        
        chat        = self._update.effective_chat
        chat_ids    = None
        chat_id     = None

        if chat.type == Chat.PRIVATE:
            chat_ids = self._context.bot_data["user_ids"]
        elif chat.typer in [Chat.GROUP, Chat.SUPERGROUP]:
            chat_ids = self._context.bot_data["group_ids"]
        else:
            chat_ids = self._context.bot_data["channel_ids"]

        for uname, cid in chat_ids:
            if uname == username:
                chat_id = cid
                break
        return chat_id

    def _send_message(self, chat_message, chat_id):
        """ It wraps send_message API 
        """

        self.logger.info(f"Sending message {chat_message} to user {self._update.effective_user.username}")
        self._context.bot.send_message(chat_id=chat_id, text=chat_message)


    def _send_message_button(self, chat_message, chat_id, attach=None, syntax=None):
        """ It wraps the message reply
        """
        self.logger.debug("Sending message '%s' for buttons" % (chat_message))
        keyboard = []
        for btnrow in attach:
            keyboard_line = []
            for btn in btnrow:
                text = btn["text"]
                callback_data = btn["callback_data"]
                keyboard_line.append(InlineKeyboardButton(text, callback_data=callback_data))
            keyboard.append(keyboard_line)
            #keyboard.append(InlineKeyboardButton(btn.label, callback_data=btn.data, callback_url=btn.url))
        reply_markup = InlineKeyboardMarkup(keyboard)
        self._update.message.reply_text(chat_message, chat_id=chat_id, reply_markup=reply_markup)
        self.logger.debug("Exiting from _send_message_button")
     

    def send(self, chat_message, chat_id=None, attach=None, syntax=None):
        
        if chat_id is None:
            chat_id = self._update.effective_chat.id

        if attach is None:
            self._send_message(chat_message, chat_id)
        else:
            self._send_message_button(chat_message, chat_id, attach._serialize_attachment()["inline_keyboard"], syntax)



