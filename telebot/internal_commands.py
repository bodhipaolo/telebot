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

from telegram       import Update
from telegram       import Chat
from telegram.ext   import CallbackContext
import botlog

logger = botlog.get_logger(__name__)

def show_chats_command(update: Update, context: CallbackContext) -> None:
        """Shows which chats the bot is in"""
        user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", dict()))
        group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", dict()))
        channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", dict()))
        text = (
            f"@{context.bot.username} bot is in contact with users {user_ids}."
            f" It is a member of the groups {group_ids}"
            f" and it is administrator in the channels {channel_ids}."
        )
        update.effective_message.reply_text(text)

def start_command(update: Update, context: CallbackContext) -> None:
    username    = update.effective_user.username
    chat        = update.effective_chat
    bot_ref     = context.bot_data.setdefault("bot_ref", dict()))
    text = (
        f"Name: {bot_ref['name]']}"
        f"Owner: {bot_ref['owner]']}"
        f"About: {bot_ref['about]']}"
    )
    update.effective_message.reply_text(text)
    logger.info(f"{username} started the bot chat")





        