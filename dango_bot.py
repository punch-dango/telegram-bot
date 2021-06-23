""" This file is modified from https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
"""
import datetime
import logging
import random

import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# preset packs
CMD_RANDOM_STICKER_SET = []
CMD_PUNCH_STICKER_SET = []
CMD_DEFEND_STICKER_SET = []
CMD_ADACHI_STICKER_SET = []
CMD_SHIMA_STICKER_SET = []
# NOTE: file_ids do not work when bot token is changed
DANGO_GIF = ['CgACAgEAAxkBAAM7YNLg_HvYfG-iZXE7TOQvbMjbPaQAAq8AA1ZqEUfsYJkqQvS3Vx8E',
             'CgACAgEAAxkBAANDYNLijfzWKs43KyoAAcc3wKwJQT6eAAKxAANWahFHIsYR4uDPfpgfBA',
             'CgACAgEAAxkBAANHYNLiok3R7uTsTwIYuqrAwo71F6AAAiMCAAKxr2lECgUL1gABNVPUHwQ',
             'CgACAgEAAxkBAANLYNLitNx9YQHaaoY7apuzHf-377oAAqEBAAJW24BENFsUZjQyHjwfBA',
             'CgACAgEAAxkBAANPYNLi1uQ5eUszbG7s0YJ39Pj_0fwAArsBAAI6euFEfbTspSwpHOsfBA',
             'CgACAgEAAxkBAANXYNLjWGQZZJT9CVEjwO6K27WF6M0AAscBAAImQJlGWyW0EyePtgIfBA']
DANGO_VIDEO = ['BAACAgEAAxkBAANfYNLliYRzXhrVBv-TOiHuAW3wryIAAjwBAALoiJhGxKUw-Bq15OIfBA']

sticker_set_cache = {}

# conversation states
MSGINFO = 1


# helper functions
def list_items(_list, _indexes):
    return [_list[i] for i in _indexes]


def append_strlist(string, strlist, indent='  '):
    if not string.endswith('\n'):
        string += '\n'
    for s in strlist:
        string += indent
        string += s
        if not s.endswith('\n'):
            string += '\n'
    return string


def combine_no_none(keys, values):
    result = []
    for k, v in zip(keys, values):
        if v:
            result.append(k + ': ' + str(v))
    return result


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("虽然我听不懂你的话，但还是先🔨🍡压惊")


def random_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(
        CMD_RANDOM_STICKER_SET), quote=False)


def punch_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(
        CMD_PUNCH_STICKER_SET), quote=False)


def defend_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(
        CMD_DEFEND_STICKER_SET), quote=False)


def adachi_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(
        CMD_ADACHI_STICKER_SET), quote=False)


def shima_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(
        CMD_SHIMA_STICKER_SET), quote=False)


def repeat_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == 1361184577:
        update.message.reply_text(" ".join(context.args), quote=False)
    else:
        update.message.reply_sticker(CMD_RANDOM_STICKER_SET[23])


def attack_command(update: Update, context: CallbackContext) -> None:
    if random.uniform(0, 1) < len(DANGO_VIDEO) / (len(DANGO_GIF) + len(DANGO_VIDEO)):
        update.message.reply_video(random.choice(DANGO_VIDEO), quote=False)
    else:
        update.message.reply_document(random.choice(DANGO_GIF), quote=False)


def send_sticker_command(update: Update, context: CallbackContext) -> None:
    try:
        pack_name = context.args[0]
        sticker_idx = int(context.args[1])
        if pack_name in sticker_set_cache:
            sticker_set = sticker_set_cache[pack_name]
        else:
            sticker_set = context.bot.get_sticker_set(pack_name).stickers
            sticker_set_cache[pack_name] = sticker_set
        update.message.reply_sticker(sticker_set[sticker_idx], quote=False)
    except:
        pass


def msginfo_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please send me a message, and I will tell you what I know about it.\n'
        'Send /cancel to stop talking to me.'
    )
    return MSGINFO


def user_info_strlist(user: telegram.User):
    keys = ['User ID', 'First Name', 'Last Name',
            'User Name', 'Language Code']
    values = [user.id, user.first_name, user.last_name,
              user.username, user.language_code]
    return combine_no_none(keys, values)


def chat_info_strlist(chat: telegram.Chat):
    keys = ['Chat ID', 'Chat Type', 'Chat Title', 'Username', 'First Name', 'Last Name', 'Bio', 'Description']
    values = [chat.id, chat.type, chat.title, chat.username, chat.first_name, chat.last_name, chat.bio,
              chat.description]
    return combine_no_none(keys, values)


def datetime_info_strlist(date: datetime.datetime):
    return [str(date)]


def doc_info_strlist(doc: telegram.Document):
    keys = ['File ID', 'File Unique ID',
            'File Name', 'Mime Type', 'File Size']
    values = [doc.file_id, doc.file_unique_id,
              doc.file_name, doc.mime_type, doc.file_size]
    return combine_no_none(keys, values)


def photo_info_strlist(photo: telegram.PhotoSize):
    keys = ['File ID', 'File Unique ID', 'Photo Width', 'Photo Height', 'File Size']
    values = [photo.file_id, photo.file_unique_id, photo.width, photo.height, photo.file_size]
    return combine_no_none(keys, values)


def video_info_strlist(video: telegram.Video):
    keys = ['File ID', 'File Unique ID', 'Video Width',
            'Video Height', 'Video Duration', 'Video Name', 'File Size']
    values = [video.file_id, video.file_unique_id, video.width, video.height, video.duration, video.file_name,
              video.file_size]
    return combine_no_none(keys, values)


def sticker_info_strlist(sticker: telegram.Sticker):
    keys = ['File ID', 'File Unique ID', 'Width', 'Height', 'File Size', 'Emoji', 'Sticker Set Name']
    values = [sticker.file_id, sticker.file_unique_id, sticker.width, sticker.height, sticker.file_size, sticker.emoji,
              sticker.set_name]
    return combine_no_none(keys, values)


def msginfo_command(update: Update, context: CallbackContext) -> int:
    result = ''

    user = update.message.from_user
    if user:
        result = 'User information about you:'
        result = append_strlist(result, user_info_strlist(user))
        update.message.reply_text(result)
    chat = update.message.chat
    if chat:
        result = 'The current chat information:'
        result = append_strlist(result, chat_info_strlist(chat))
        update.message.reply_text(result)
    date = update.message.date
    if date:
        result = 'The message is sent on:'
        result = append_strlist(result, datetime_info_strlist(date))
        update.message.reply_text(result)
    doc = update.message.document
    if doc:
        result = 'The message contains a document:'
        result = append_strlist(result, doc_info_strlist(doc))
        update.message.reply_text(result)
    photos = update.message.photo
    if photos:
        for idx, photo in enumerate(photos):
            result = f'Photo #{idx + 1}:'
            result = append_strlist(result, photo_info_strlist(photo))
            update.message.reply_text(result)
    video = update.message.video
    if video:
        result = 'The message contains a video:'
        result = append_strlist(result, video_info_strlist(video))
        update.message.reply_text(result)
    sticker = update.message.sticker
    if sticker:
        result = 'The message contains a sticker:'
        result = append_strlist(result, sticker_info_strlist(sticker))
        update.message.reply_text(result)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END


def initialize_stickers(bot):
    dango_sticker_set = bot.get_sticker_set('tuanzi_public').stickers
    adashima_sticker_set = bot.get_sticker_set('adashima').stickers

    global CMD_RANDOM_STICKER_SET
    global CMD_PUNCH_STICKER_SET
    global CMD_DEFEND_STICKER_SET
    global CMD_ADACHI_STICKER_SET
    global CMD_SHIMA_STICKER_SET

    CMD_RANDOM_STICKER_SET = dango_sticker_set
    CMD_PUNCH_STICKER_SET = list_items(dango_sticker_set, [
        1, 11, 19, 23, 28, 30, 40, 47, 48, 59, 60, 62, 63, 64, 65, 66, 67, 68, 85, 86, 87, 96, 99])
    CMD_DEFEND_STICKER_SET = list_items(dango_sticker_set, [
        3, 9, 10, 13, 14, 16, 22, 26, 32, 33, 36, 41, 42, 44, 71, 75, 82, 97]) + list_items(adashima_sticker_set,
                                                                                            [1, 5, 15, 16, 20, 37])
    CMD_ADACHI_STICKER_SET = list_items(adashima_sticker_set, [
        0, 2, 5, 6, 8, 9, 14, 15, 16, 18, 20, 22, 24, 26, 28, 29, 31, 33, 38])
    CMD_SHIMA_STICKER_SET = list_items(adashima_sticker_set, [
        1, 3, 4, 7, 10, 13, 19, 21, 23, 25, 27, 29, 30, 32, 33, 34, 35, 37, 39])


def main() -> None:
    updater = Updater("TOKEN")
    bot = updater.bot
    initialize_stickers(bot)

    # conversations
    msginfo_handler = ConversationHandler(
        entry_points=[CommandHandler('msginfo', msginfo_start)],
        states={
            MSGINFO: [MessageHandler(~Filters.command, msginfo_command)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("random", random_command))
    dispatcher.add_handler(CommandHandler("punch", punch_command))
    dispatcher.add_handler(CommandHandler("defend", defend_command))
    dispatcher.add_handler(CommandHandler("adachi", adachi_command))
    dispatcher.add_handler(CommandHandler("shima", shima_command))
    dispatcher.add_handler(CommandHandler("repeat", repeat_command))
    dispatcher.add_handler(CommandHandler("attack", attack_command))
    dispatcher.add_handler(CommandHandler(
        "send_sticker", send_sticker_command))
    dispatcher.add_handler(msginfo_handler)
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
