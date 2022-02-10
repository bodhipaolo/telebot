from queue 		import Queue
from threading 	import Thread


class ConsumerManager:

	def __init__ (self, num_threads = 10, queue_size = 0):
		self._num_threads	= num_threads
		self._queue_size	= queue_size 
		self.consumers 		= []
		self.queue 			= None
		
	def initialize(self):
		self.queue = Queue(maxsize = self._queue_size)
		for i in range (self._num_threads):
			consumer = Consumer(self.queue)
			consumer.setDaemon(True)
			self.consumers.append(consumer)

	def start(self):
		for consumer in self.consumers:
			consumer.start()

class Consumer(Thread):

	def __init__(self, queue):
		super().__init__()
		self._queue = queue

	def run(self):
		while True:
			task = self._queue.get()
			if task is not None:
				task.execute()

class BotTask:
	
	def __init__(self, name, user_callback):
		self.name 			= name
		self._user_callback	= user_callback

class CommandTask(BotTask):
	
	def __init__(self, name, user_callback, chat, message, args):
		super().__init__(name, user_callback)
		self._chat 		= chat
		self._message	= message
		self._args		= args

	def execute(self):
		super().user_callback(self._chat, self._message, self._args)

class MessageMatchTask(BotTask):
	
	def __init__(self, name, user_callback, chat, message, matches):
		super().__init__(name, user_callback)
		self._chat 		= chat
		self._message	= message
		self._matches	= matches

	def execute(self):
		super().user_callback(self._chat, self._message, self._matches)

class MessageTask(BotTask):
	
	def __init__(self, name, user_callback, chat, message):
		super().__init__(name, user_callback)
		self._chat 		= chat
		self._message	= message

	def execute(self):
		super().user_callback(self._chat, self._message)

class CallabckTask(BotTask):
	
	def __init__(self, name, user_callback, query, data, chat, message):
		super().__init__(name, user_callback)
		self._query 	= query
		self._data		= data
		self._chat 		= chat
		self._message	= message

	def execute(self):
		super().user_callback(self._query, self._data, self._chat, self._message)

