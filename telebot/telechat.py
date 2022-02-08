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
    
    def _send_message(self, chat_message):
        """ It wraps send_message API 
        """
        self.logger.debug("Sending message '%s'" % (chat_message))
        self._context.bot.send_message(chat_id=self._update.effective_chat.id, text=chat_message)
        
    def _send_message_button(self, chat_message, attach=None, syntax=None):
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
        self._update.message.reply_text(chat_message, reply_markup=reply_markup)
        self.logger.debug("Exiting from _send_message_button")
        
    def send(self, chat_message, attach=None, syntax=None):
        if attach is None:
            self._send_message(chat_message)
        else:
            self._send_message_button(chat_message, attach._serialize_attachment()["inline_keyboard"], syntax)



