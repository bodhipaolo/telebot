from queue 			import Queue
from telegram       import Update
from telegram.ext   import Updater
from telegram.ext   import CallbackContext
from telegram.ext   import CommandHandler

import botlog
from telechat       import Telechat
from messages    	import TextMessage


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
		self.logger.debug ("Enter command listener")
		chat = Telechat(update, context)
		if update.message != None:
			message = TextMessage(update.message.message_id, update.message.date, update.message.text)
		else:
			message = None

		task = CommandTask(self.name, super()._user_callback, chat, message, context.args)
		self._consumer_manager.queue.put(task)

class MessageMatchListener(BotListener):
	""" Task for handling messages callback and matches
	"""

	def listener(self, update: Update, context: CallbackContext):
		"""Message match decoretor. It is a callback that intercepts the event of message matching
		"""
		self.logger.debug ("Enter message matches listener")
		chat = Telechat(update, context)
		self.logger.debug ("Enter message matches listener")
		chat = Telechat(update, context)
		if update.message != None:
			message = TextMessage(update.message.message_id, update.message.date, update.message.text)
		else:
			message = None

		task = MessageMatchTask(super().name, super()._user_callback, chat, message, context.matches)
		self._consumer_manager.queue.put(task)


class MessageListener(BotListener):
	""" Task for handling messages callback and matches
	"""

	def listener(self, update: Update, context: CallbackContext):
		"""Message match decoretor. It is a callback that intercepts the event of message matching
		"""
		self.logger.debug ("Enter message matches listener")
		chat = Telechat(update, context)
		if update.message != None:
			message = TextMessage(update.message.message_id, update.message.date, update.message.text)
		else:
			message = None

		task = MessageTask(super().name, super()._user_callback, chat, message)
		self._consumer_manager.queue.put(task)


class CallbackListener(BotListener):
	""" Task for handling command callback
	"""

	def listener(self, update: Update, context: CallbackContext):
		"""Command decoretor. It is a callback that intercept the event and map parameter for the client callback
		"""
		query = update.callback_query
		if query.data == self.callback_name:
			self.logger.debug ("Enter callback listener for %s" % self.callback_name)
			data = query.data
			chat = Telechat(update, context)
			if update.message != None:
				message = TextMessage(update.message.message_id, update.message.date, update.message.text)
			else:
				message = None

			task = CallabckTask(super().name, super()._user_callback, query, data, chat, message)
			self._consumer_manager.queue.put(task)



