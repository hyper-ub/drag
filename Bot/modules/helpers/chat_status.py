from functools import wraps

from Bot import dispatcher,OWNER_ID
from telegram import Chat, ChatMember, ParseMode, Update
from telegram.ext import CallbackContext

DRAGONS = OWNER_ID


DEL_CMDS= True
def user_admin(func):
    @wraps(func)
    def is_admin(update: Update, context: CallbackContext, *args, **kwargs):
        bot = context.bot
        user = update.effective_user
        chat = update.effective_chat

        if user and is_user_admin(chat, user.id):
            return func(update, context, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()
        else:
            update.effective_message.reply_text(
                "Who dis non-admin telling me what to do? You want a punch?")

    return is_admin


def user_admin_no_reply(func):

    @wraps(func)
    def is_not_admin_no_reply(update: Update, context: CallbackContext, *args,
                              **kwargs):
        bot = context.bot
        user = update.effective_user
        chat = update.effective_chat

        if user and is_user_admin(chat, user.id):
            return func(update, context, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()

    return is_not_admin_no_reply


def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (chat.type == 'private' or user_id in [OWNER_ID] or
            chat.all_members_are_administrators or
            user_id in [777000, 1087968824
                       ]):  # Count telegram and Group Anonymous as admin
        return True

    if not member:
        member = chat.get_member(user_id)

    return member.status in ('administrator', 'creator')

