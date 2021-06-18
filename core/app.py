#!/usr/bin/env python3
import logging
import os
from functools import wraps
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from celery import Celery
from celery import chain
import validators
capp = Celery(broker="redis://localhost:6379", backend="redis://localhost:6379")
capp.conf['result_expires'] = 60*10
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.environ["TOKEN"]


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Enter a domain name:')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use /start command to use reconflow')


@send_typing_action
def echo(update, context):
    chat_id = update.message.chat.id
    sig_list = []
    domain = update.message.text
    if validators.domain(domain):
        sub_sig = capp.signature('core.subdomains', debug=True,
                                 args=[domain, chat_id]).set(queue='core')
        sig_list.append(sub_sig)

        live_sig = capp.signature('core.livedomains', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(live_sig)

        ports_sig = capp.signature('core.ports', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(ports_sig)

        dir_sig = capp.signature('core.directories', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(dir_sig)

        chain(sig_list).apply_async()
        update.message.reply_text(f"Report for domain {domain} will be sent soon!")
    else:
        update.message.reply_text(f"Use a valid domain name without http:// or https:// & try again!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
