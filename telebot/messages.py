class Message:
	""" Abstract message class
	"""
	def __init__(self, message_id, date):
		self.message_id 	= message_id
		self.date 		 	= date


class TextMessage(Message):
	""" Concrete Message class for text messages
	"""
	def __init__(self, message_id, date, text):
		super().__init__(message_id, date)
		self.text = text 



