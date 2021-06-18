#!/usr/bin/env python3
import logging
import os
from functools import wraps
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram import ChatAction, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from celery import Celery
from celery import chain
import validators
capp = Celery(broker="redis://localhost:6379", backend="redis://localhost:6379")
capp.conf['result_expires'] = 60*10
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.environ["TOKEN"]

DOMAIN, CHOOSING = range(2)

reply_keyboard = [
    ['Subdomain Enummeration', 'Livedomain Enumeration'],
    ['Port Scanning', 'Directory Bruteforcing'],
    ['Run all the phases'],
    ['Cancel']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def start(update, context):
    """Send a message when the command /start is issued."""
    message = """
              Hello I'm the ReconFlow bot. I would be more than happy to serve you.
              To proceed please enter a valid domain name.  
              """
    update.message.reply_text(message)
    user_data = context.user_data
    user_data['domain'] = update.message.text
    del user_data['choice']
    return DOMAIN


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use /start command to use reconflow')


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        f"Thank you for using ReconFlow. See you around!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def domain(update, context):
    domain = update.message.text
    if validators.domain(domain):
        message = """
                  Which phase do you want the report for?
                  """
        update.message.reply_text(message, reply_markup=markup)
        return CHOOSING
    else:
        update.message.reply_text(f"Use a valid domain name without http:// or https:// & try again!",
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


@send_typing_action
def choice(update, context):
    chat_id = update.message.chat.id
    user_data = context.user_data
    domain = user_data["domain"]
    choice = update.message.text
    if choice == "Run all the phases":
        sig_list = []
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
        update.message.reply_text(f"Report for all of the phases for domain {domain} will be sent soon!")
    elif choice == "Subdomain Enummeration":
        sig_list = []
        sub_sig = capp.signature('core.subdomains', debug=True,
                                 args=[domain, chat_id]).set(queue='core')
        sig_list.append(sub_sig)

        chain(sig_list).apply_async()
        update.message.reply_text(f"Subdomain Enummeration Report for domain {domain} will be sent soon!")
    elif choice == "Livedomain Enumeration":
        sig_list = []
        sub_sig = capp.signature('core.subdomains', debug=True,
                                 args=[domain, chat_id]).set(queue='core')
        sig_list.append(sub_sig)

        live_sig = capp.signature('core.livedomains', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(live_sig)

        chain(sig_list).apply_async()
        update.message.reply_text(f"Livedomain Enumeration Report for domain {domain} will be sent soon!")
    elif choice == "Port Scanning":
        sig_list = []
        sub_sig = capp.signature('core.subdomains', debug=True,
                                 args=[domain, chat_id]).set(queue='core')
        sig_list.append(sub_sig)

        ports_sig = capp.signature('core.ports', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(ports_sig)

        chain(sig_list).apply_async()
        update.message.reply_text(f"Subdomain Enummeration Report for domain {domain} will be sent soon!")
    elif choice == "Directory Bruteforcing":
        sig_list = []
        sub_sig = capp.signature('core.subdomains', debug=True,
                                 args=[domain, chat_id]).set(queue='core')
        sig_list.append(sub_sig)

        live_sig = capp.signature('core.livedomains', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(live_sig)

        dir_sig = capp.signature('core.directories', debug=True, args=[chat_id]).set(queue='core')
        sig_list.append(dir_sig)

        chain(sig_list).apply_async()
        update.message.reply_text(f"Subdomain Enummeration Report for domain {domain} will be sent soon!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            DOMAIN: [MessageHandler(Filters.text, domain)],
            CHOOSING: [MessageHandler(
                    Filters.regex('^(Subdomain Enummeration|Livedomain Enumeration|Port Scanning|'
                                  'Directory Bruteforcing|Run all the phases)$'), choice
                )],
        },

        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('help', help)]
    )
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
