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
from telegram.ext   import CallbackContext

def show_chats_command(update: Update, context: CallbackContext) -> None:
        """Shows which chats the bot is in"""
        user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", dict()))
        group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", dict()))
        channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", dict()))
        text = (
            f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
            f" Moreover it is a member of the groups with IDs {group_ids}."
            f"and administrator in the channels with IDs {channel_ids}."
        )
        update.effective_message.reply_text(text)