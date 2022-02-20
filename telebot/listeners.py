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

from typing         import Tuple, Optional
from queue          import Queue
from telegram       import Update
from telegram       import ChatMemberUpdated
from telegram.ext   import Updater
from telegram.ext   import CallbackContext
from telegram.ext   import CommandHandler

import botlog
from telechat       import Telechat
from messages       import TextMessage
from consumers      import CommandTask
from consumers      import MessageMatchTask
from consumers      import MessageContainsTask
from consumers      import CallbackTask
from consumers      import InternalCommandTask

logger = botlog.get_logger(__name__)


class BotListener:
    """Generic class Task to be subclasses for specific implementations (i.e.: CommandTask, MessageMatchTask...)
    """

    def __init__(self, user_callback, consumer_manager):
        self._user_callback     = user_callback
        self._consumer_manager  = consumer_manager

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


class MessageContainsListener(BotListener):
    """ Task for handling messages callback and matches
    """
    def __init__(self, user_callback, token, consumer_manager):
        super().__init__(user_callback, consumer_manager)
        self.token = token

    def listener(self, update: Update, context: CallbackContext):
        """Message match decoretor. It is a callback that intercepts the event of message matching
        """
        if (update.message is not None):
            logger.info(f"Enter message listener for {update.message.text}")
            if self.token in f" {update.message.text} ": 
                chat = Telechat(update, context)
                message = TextMessage(update.message.message_id, update.message.date, update.message.text)
                task = MessageContainsTask(self._user_callback, chat, message)
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
        prefix_data = query.data.split('_',1)[0]
        if prefix_data == self.callback_name:
            logger.debug (f"Enter callback listener for {self.callback_name}")
            data = query.data
            chat = Telechat(update, context)
            if update.message != None:
                message = TextMessage(update.message.message_id, update.message.date, update.message.text)
            else:
                message = None

            task = CallabckTask(self._user_callback, query, data, chat, message)
            self._consumer_manager.queue.put(task)

class ChatMemberListener(BotListener):
    """ Task for handling messages callback and matches
    """
    def __init__(self):
        # Non need to store callback since it is not driven by client programming (no deorator)
        super().__init__(None, None)

    def _extract_status_change(self, chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]: 
        """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
        of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
        the status didn't change.
        """
        status_change = chat_member_update.difference().get("status")
        old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

        if status_change is None:
            return None

        old_status, new_status = status_change
        was_member = (
            old_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (old_status == ChatMember.RESTRICTED and old_is_member is True)
        )
        is_member = (
            new_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (new_status == ChatMember.RESTRICTED and new_is_member is True)
        )

        return was_member, is_member

    def _show_chats(update: Update, context: CallbackContext) -> None:
        """Shows which chats the bot is in"""
        user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", dict()))
        group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", dict()))
        channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", dict()))
        text = (
            f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
            f" Moreover it is a member of the groups with IDs {group_ids} "
            f"and administrator in the channels with IDs {channel_ids}."
        )
        update.effective_message.reply_text(text)

    def _track_chats(self, update: Update, context: CallbackContext) -> None:
        """Tracks the chats the bot is in."""
        result = self._extract_status_change(update.my_chat_member)
        if result is None:
            return
        was_member, is_member = result

        # Let's check who is responsible for the change
        username = update.effective_user.username

        # Handle chat types differently:
        chat = update.effective_chat
        if chat.type == Chat.PRIVATE:
            if not was_member and is_member:
                logger.info("%s started the bot", username)
                context.bot_data.setdefault("user_ids", dict())
                context.bot_data["user_ids"][username] = chat.id
            elif was_member and not is_member:
                logger.info("%s blocked the bot", username)
                context.bot_data.setdefault("user_ids", dict())
                context.bot_data["user_ids"].pop(username, None)

        elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            if not was_member and is_member:
                logger.info("%s added the bot to the group %s", username, chat.title)
                context.bot_data.setdefault("group_ids", dict())
                context.bot_data["group_ids"][username] = chat.id
            elif was_member and not is_member:
                logger.info("%s removed the bot from the group %s", username, chat.title)
                context.bot_data["group_ids"].pop(username, None)
        else:
            if not was_member and is_member:
                logger.info("%s added the bot to the channel %s", username, chat.title)
                context.bot_data.setdefault("channel_ids", dict())
                context.bot_data["channel_ids"][username] = chat.id
            elif was_member and not is_member:
                logger.info("%s removed the bot from the channel %s", username, chat.title)
                context.bot_data["channel_ids"].pop(username, None)

    
    def listener(self, update: Update, context: CallbackContext):
        """Message match decoretor. It is a callback that intercepts the event of message matching
        """
        
        # It runs in the main thread
        logger.info("Entering ChatMemberListener listener callback")
        self._track_chats(update, context)

class InternalCommandListener(BotListener):
    """ Task for handling command callback
    """
    def __init__(self, call_name, user_callback, consumer_manager):
        super().__init__(user_callback, consumer_manager)
        self.name = call_name

    def listener(self, update: Update, context: CallbackContext):
        """Command decoretor. It is a callback that intercept the event and map parameter for the client callback
        """
        task = InternalCommandTask(self._user_callback, update, context)
        self._consumer_manager.queue.put(task)
        


