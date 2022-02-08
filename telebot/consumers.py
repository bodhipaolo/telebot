from Queue import Queue
from threading import Thread

class Consumer(Thread):

	def __init__(self, queue):
		super().__init__()
		self._queue = queue

	def run(self):
		while True:
			task = self._queue.get()
			if task is not None:
				task.execute()

class ConsumerManager:

	def __init__ (self, num_threads = 10, queue_size = 0):
		self._num_threads	= num_threads
		self._queue_size	= queue_size 
		self.consumers 		= []
		self.queue 			= None
		
	def initialize(self):
		self.queue = Queue(maxsize = self._queue_size)
		for i in range (self._num_threads):
			consumer = Consumer(self._queue)
			consumer.setDaemon(True)
			consumers.append(consumer)

	def start():
		for consumer in consumers:
			consumer.start()

class BotTask:
	
	def __init__(self, name, user_callback):
		self._name 			= name
		self._user_callback	= user_callback

class CommandTask(BotTask):
	
	def __init__(self, name, usercallback, chat, message, args):
		super().__init__(name, user_callback)
		self._chat 		= chat
		self._message	= message
		self._args		= args

	def execute(self):
		super().user_callback(chat, message, args)



