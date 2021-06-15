""" This file is modified from https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
"""
import logging
import random

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CMD_RANDOM_STICKER_SET = []
CMD_PUNCH_STICKER_SET = []
CMD_DEFEND_STICKER_SET = []
CMD_ADACHI_STICKER_SET = []
CMD_SHIMA_STICKER_SET = []


def list_items(_list, _indexes):
    return [_list[i] for i in _indexes]


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("虽然我听不懂你的话，但还是先🔨🍡压惊")


def random_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(CMD_RANDOM_STICKER_SET))


def punch_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(CMD_PUNCH_STICKER_SET))


def defend_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(CMD_DEFEND_STICKER_SET))


def adachi_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(CMD_ADACHI_STICKER_SET))


def shima_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker(random.choice(CMD_SHIMA_STICKER_SET))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")
    bot = updater.bot

    dango_sticker_set = bot.get_sticker_set('tuanzi_public').stickers
    adashima_sticker_set = bot.get_sticker_set('adashima').stickers

    global CMD_RANDOM_STICKER_SET
    global CMD_PUNCH_STICKER_SET
    global CMD_DEFEND_STICKER_SET
    global CMD_ADACHI_STICKER_SET
    global CMD_SHIMA_STICKER_SET

    CMD_RANDOM_STICKER_SET = dango_sticker_set
    CMD_PUNCH_STICKER_SET = list_items(
        dango_sticker_set, [1, 11, 19, 23, 28, 30, 40, 47, 48, 59, 60, 62, 63, 64, 65, 66, 67, 68, 85, 86, 87, 96, 99])
    CMD_DEFEND_STICKER_SET = list_items(dango_sticker_set, [
                                        3, 9, 10, 13, 14, 16, 22, 26, 32, 33, 36, 41, 42, 44, 71, 75, 82, 97]) + list_items(adashima_sticker_set, [1, 5, 15, 16, 20, 37])
    CMD_ADACHI_STICKER_SET = list_items(adashima_sticker_set, [
                                        0, 2, 5, 6, 8, 9, 14, 15, 16, 18, 20, 22, 24, 26, 28, 29, 31, 33, 38])
    CMD_SHIMA_STICKER_SET = list_items(adashima_sticker_set, [
                                       1, 3, 4, 7, 10, 13, 19, 21, 23, 25, 27, 29, 30, 32, 33, 34, 35, 37, 39])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("random", random_command))
    dispatcher.add_handler(CommandHandler("punch", punch_command))
    dispatcher.add_handler(CommandHandler("defend", defend_command))
    dispatcher.add_handler(CommandHandler("adachi", adachi_command))
    dispatcher.add_handler(CommandHandler("shima", shima_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
