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

from queue      import Queue
from threading  import Thread
import botlog

logger = botlog.get_logger(__name__)

class StopSignal:
    pass

class ConsumerManager:

    def __init__ (self, num_threads = 10, queue_size = 0):
        self._num_threads   = num_threads
        self._queue_size    = queue_size 
        self.consumers      = []
        self.queue          = None
      
    def _insertStops(self):
        for i in range(self._num_threads):
            self.queue.put(StopSignal())

    def initialize(self):
        self.queue = Queue(maxsize = self._queue_size)
        for i in range (self._num_threads):
            consumer = Consumer(self.queue, f"thread-{i}")
            consumer.setDaemon(True)
            self.consumers.append(consumer)

    def start(self):
        logger.info("%s Starting Consumer threads." % (__name__))
        for consumer in self.consumers:
            consumer.start()
            logger.info(f"{consumer.name} started.")

    def stop(self):
        logger.info("%s Stopping Consumer threads." % (__name__))
        self._insertStops()
        for consumer in self.consumers:
            consumer.join()
            logger.info(f"{consumer.name} stopped.")

class Consumer(Thread):

    def __init__(self, queue, name):
        super().__init__(name = name)
        self._queue = queue

    def run(self):
        while True:
            task = self._queue.get()
            if task is not None:
                if type(task) is StopSignal:
                    logger.debug(f"Exiting run from thread: {super().name}")
                    break
                task.execute()

class BotTask:
    
    def __init__(self, user_callback):
        self._user_callback = user_callback

class CommandTask(BotTask):
    
    def __init__(self, user_callback, chat, message, args):
        super().__init__(user_callback)
        self._chat      = chat
        self._message   = message
        self._args      = args

    def execute(self):
        self._user_callback(self._chat, self._message, self._args)

class MessageMatchTask(BotTask):
    
    def __init__(self, user_callback, chat, message, matches):
        super().__init__(user_callback)
        self._chat      = chat
        self._message   = message
        self._matches   = matches

    def execute(self):
        self._user_callback(self._chat, self._message, self._matches)

class MessageContainsTask(BotTask):
    
    def __init__(self, user_callback, chat, message):
        super().__init__(user_callback)
        self._chat      = chat
        self._message   = message

    def execute(self):
        self._user_callback(self._chat, self._message)

class CallbackTask(BotTask):
    
    def __init__(self, user_callback, query, data, chat, message):
        super().__init__(user_callback)
        self._query     = query
        self._data      = data
        self._chat      = chat
        self._message   = message

    def execute(self):
        self._user_callback(self._query, self._data, self._chat, self._message)

class InternalCommandTask(BotTask):
    
    def __init__(self, user_callback, update, context):
        super().__init__(user_callback)
        self._update    = update
        self._context   = context

    def execute(self):
        self._user_callback(self._update, self._context)

