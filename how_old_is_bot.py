import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests


TOKEN = os.environ.get('HOW_OLD_IS_TOKEN')

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater.start_polling()


def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Who's age would you like to know? Type /how_old_is [enter person's name]")

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def find_age(content, age_tag):
    find_age = content.split(age_tag)[1]
    age = find_age.split(')<')[0]
    return age

def how_old_is(name):
    name = ' '.join(name).title()
    r = requests.get('https://en.wikipedia.org/wiki/' + name)
    content = r.text
    age_tag = '>(age&#160;'
    if age_tag not in content:
        death__age_tag = '> (aged&#160;'
        if death__age_tag not in content:
            return "Sorry, I could not locate {}\'s age".format(name)
        age_at_death = find_age(content, death__age_tag)
        return '{} died at age {}'.format(name, age_at_death)
    age = find_age(content, age_tag)
    return '{} is {} years old'.format(name, age)

def how_old_is_answer(bot, update, args):
    answer = how_old_is(args)
    bot.sendMessage(chat_id=update.message.chat_id, text=answer)

how_old_is_answer_handler = CommandHandler('how_old_is', how_old_is_answer, pass_args=True)
dispatcher.add_handler(how_old_is_answer_handler)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)