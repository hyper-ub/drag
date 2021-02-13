import requests
import random
import nekos
from PIL import Image
import os
from Bot.modules.sql.users_sql import get_all_users
from telegram import Message, Chat, Update, Bot, MessageEntity
import Bot.modules.fun_strings as fun_strings
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async,CallbackContext

from Bot import dispatcher, updater


def is_user_in_chat(chat: Chat, user_id: int) -> bool:
    member = chat.get_member(user_id)
    return member.status not in ("left", "kicked")
def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith('@'):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = dispatcher.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    LOGGER.exception("Error extracting user ID")

    return None


HUGS = (
    "⊂(・﹏・⊂)",
    "⊂(・ヮ・⊂)",
    "⊂(・▽・⊂)",
    "(っಠ‿ಠ)っ",
    "ʕっ•ᴥ•ʔっ",
    "（っ・∀・）っ",
    "(っ⇀⑃↼)っ",
    "(つ´∀｀)つ",
    "(.づσ▿σ)づ.",
    "⊂(´・ω・｀⊂)",
    "(づ￣ ³￣)づ",
    "(.づ◡﹏◡)づ.",
)


@run_async
def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_SAITAMA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False))
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    if update.effective_user.id == 1625230499 :
        temp = "my bat  scratches {user2}"

    reply = temp.format(
        user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)








@run_async
def neko(update, context):
    msg = update.effective_message
    target = "neko"
    msg.reply_photo(nekos.img(target))


    
@run_async
def kill(update: Update, context: CallbackContext):
    message = update.effective_message
    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    reply_animation = message.reply_to_message.reply_animation if message.reply_to_message else message.reply_animation
    reply_animation(
        random.choice(fun.DEATHGIF))




@run_async
def wallpaper(update, context):
    msg = update.effective_message
    target = "wallpaper"
    msg.reply_photo(nekos.img(target))



@run_async
def tickle(update, context):
    msg = update.effective_message
    target = "tickle"
    msg.reply_video(nekos.img(target))


@run_async
def poke(update, context):
    msg = update.effective_message
    target = "poke"
    msg.reply_video(nekos.img(target))


@run_async
def waifu(update, context):
    msg = update.effective_message
    target = "waifu"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def kiss(update, context):
    msg = update.effective_message
    target = "kiss"
    msg.reply_video(nekos.img(target))

@run_async
def baka(update, context):
    msg = update.effective_message
    target = "baka"
    msg.reply_video(nekos.img(target))

@run_async
def feed(update, context):
    msg = update.effective_message
    target = "feed"
    msg.reply_video(nekos.img(target))

@run_async
def hug(update: Update, context: CallbackContext):
    # reply to correct message
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text = reply_text(random.choice(HUGS))

@run_async
def cuddle(update, context):
    msg = update.effective_message
    target = "cuddle"
    msg.reply_video(nekos.img(target))



NEKO_HANDLER = CommandHandler("neko", neko)
CUDDLE_HANDLER = CommandHandler("hug", cuddle)
#PAT_HANDLER = CommandHandler("pat", pat)
SLAP_HANDLER = CommandHandler("slap", slap)
WALLPAPER_HANDLER = CommandHandler("wallpaper", wallpaper)
TICKLE_HANDLER = CommandHandler("tickle", tickle)
FEED_HANDLER = CommandHandler("feed", feed)
POKE_HANDLER = CommandHandler("poke", poke)
WAIFU_HANDLER = CommandHandler("waifu", waifu)
KISS_HANDLER = CommandHandler("kiss", kiss)
BAKA_HANDLER = CommandHandler("baka", baka)


dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(BAKA_HANDLER)
dispatcher.add_handler(KISS_HANDLER)
dispatcher.add_handler(CUDDLE_HANDLER)
#dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(WAIFU_HANDLER)
dispatcher.add_handler(POKE_HANDLER)
dispatcher.add_handler(FEED_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(TICKLE_HANDLER)


__help__ = """
-/neko :- send swf images
-/hug. :- hug user
-/baka ;- send baka 
-/kiss :- kiss user
-/pat  :- pat a user
-/waifu :- get waifu images
-/slap  :- slap a user
-/poko  :- poke a user
-/feed :- feed a user.
-/wallpaper :- get wallpaper
-/kill :- get kill gifs
-/tickle :- tickle a user
"""




__mod_name__ = "fun"

