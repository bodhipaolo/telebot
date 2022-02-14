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

from queue 			import Queue
from telegram       import Update
from telegram.ext   import Updater
from telegram.ext   import CallbackContext
from telegram.ext   import CommandHandler

import botlog
from telechat       import Telechat
from messages    	import TextMessage
from consumers		import CommandTask
from consumers		import MessageMatchTask
from consumers		import MessageTask
from consumers		import CallabckTask

logger = botlog.get_logger(__name__)

class BotListener:
	"""Generic class Task to be subclasses for specific implementations (i.e.: CommandTask, MessageMatchTask...)
	"""

	def __init__(self, user_callback, consumer_manager):
		self._user_callback 	= user_callback
		self._consumer_manager 	= consumer_manager

	def listener(self, update: Update, context: CallbackContext):
		print ("Throw an expection here")

class CommandListener(BotListener):
	""" Task for handling command callback
	"""
	def __init__(self, name, user_callback, consumer_manager):
		super().__init__(user_callback, consumer_manager)
		self.name = name

	def listener(self, update: Update, context: CallbackContext):
		"""Command decoretor. It is a callback that intercept the event and map parameter for the client callback
		"""
		if (update.message is not None):
			name = update.message.text
		logger.info(f"Enter command listener for {name}")
		chat = Telechat(update, context)
		if update.message != None:
			message = TextMessage(update.message.message_id, update.message.date, update.message.text)
		else:
			message = None
		task = CommandTask(self._user_callback, chat, message, context.args)
		self._consumer_manager.queue.put(task)

class MessageMatchListener(BotListener):
	""" Task for handling messages callback and matches
	"""
	def __init__(self, user_callback, regex, consumer_manager):
		super().__init__(user_callback, consumer_manager)
		self._regex = regex

	def listener(self, update: Update, context: CallbackContext):
		"""Message match decoretor. It is a callback that intercepts the event of message matching
		"""
		if (update.message is not None):
			name = update.message.text
		logger.info(f"Enter message_match listener for {name}")
		chat = Telechat(update, context)
		chat = Telechat(update, context)
		if update.message != None:
			message = TextMessage(update.message.message_id, update.message.date, update.message.text)
		else:
			message = None

		task = MessageMatchTask(self._user_callback, chat, message, context.matches)
		self._consumer_manager.queue.put(task)


class MessageListener(BotListener):
	""" Task for handling messages callback and matches
	"""

	def listener(self, update: Update, context: CallbackContext):
		"""Message match decoretor. It is a callback that intercepts the event of message matching
		"""
		if (update.message is not None):
			name = update.message.text
		logger.info(f"Enter message listener for {name}")
		chat = Telechat(update, context)
		if update.message != None:
			message = TextMessage(update.message.message_id, update.message.date, update.message.text)
		else:
			message = None

		task = MessageTask(self._user_callback, chat, message)
		self._consumer_manager.queue.put(task)


class CallbackListener(BotListener):
	""" Task for handling command callback
	"""
	def __init__(self, name, user_callback, consumer_manager):
		super().__init__(user_callback, consumer_manager)
		self.callback_name = name

	def listener(self, update: Update, context: CallbackContext):
		"""Command decoretor. It is a callback that intercept the event and map parameter for the client callback
		"""
		query = update.callback_query
		if query.data.startswith(self.callback_name):
			logger.debug (f"Enter callback listener for {self.callback_name}")
			data = query.data
			chat = Telechat(update, context)
			if update.message != None:
				message = TextMessage(update.message.message_id, update.message.date, update.message.text)
			else:
				message = None

			task = CallabckTask(self._user_callback, query, data, chat, message)
			self._consumer_manager.queue.put(task)



