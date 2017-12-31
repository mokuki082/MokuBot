#!/usr/bin/env python3

import json
import threading
from datetime import datetime
import logging

# Global Variables
VERSION = '1.0.0'
HAS_TELEGRAM = True

try:
    from telegram.error import InvalidToken
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
except ImportError:
    HAS_TELEGRAM = False


class MokuBot():

    """ Stores and executes functionalities of MokuBot """

    def __init__(self, token):

        """ Constructor

        Keyword arguments:
        token -- Telegram Bot token
        """

        self.start_time = datetime.now()

        # Initialize updater
        try:
            self.updater = Updater(token)
        except InvalidToken:
            print("The token you are using is invalid.")
            print("Please ask for a token from @BotFather", end=' ')
            print('and replace your token at config.json')
            exit(1)

        hello_handler = CommandHandler('uptime', self.uptime)
        self.updater.dispatcher.add_handler(hello_handler)
        # Unknown commands
        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.updater.dispatcher.add_handler(unknown_handler)

    def stop(self):

        """ Stop polling updates """

        self.updater.stop()

    def uptime(self, bot, update):

        """ uptime command handler

        Keyword arguments:
        bot -- A dictionary containing bot information
        update -- a dictionary containing command sender's information
        """

        td = datetime.now() - self.start_time
        days = td.days
        hours = td.seconds // 3600
        minutes = td.seconds // 60 % 60
        seconds = td.seconds % 60

        text = 'MokuBot has been up for '
        if days == 0 or days > 1:
            text += '{} days '.format(days)
        else:
            text += '{} day '.format(days)
        if hours == 0 or hours > 1:
            text += '{} hours '.format(hours)
        else:
            text += '{} hour '.format(hours)
        if minutes == 0 or minutes > 1:
            text += '{} minutes '.format(minutes)
        else:
            text += '{} minute '.format(minutes)
        if seconds == 0 or seconds > 1:
            text += '{} seconds.'.format(seconds)
        else:
            text += '{} second.'.format(seconds)
        update.message.reply_text(text)

    def unknown(self, bot, update):

        """ Known command handler

        Keyword arguments:
        bot -- A dictionary containing bot information
        update -- a dictionary containing command sender's information
        """

        text = 'Sorry, I didn\'t understand that command.'
        update.message.reply_text(text)

    def run(self):
        """ Start polling updates """
        self.updater.start_polling(poll_interval=0.5)


def command_engine(mokubot):

    """ Continuously ask for commands until 'stop' is entered via stdin """

    print("Welcome to MokuBot. Enter 'help' for list of commands.")

    while True:
        command = input("\nConsole: ")
        if command == 'help':
            print('List of commands:')
            print('stop - stops the program')
        elif command == 'stop':
            print('Stopping MokuBot, please wait...')
            mokubot.stop()
            break
        else:
            print('Invalid command. Enter \'help\' for list of commands.')

def generate_config():

    """ Generate config file and save it in config.json """

    global VERSION
    config = {'version': VERSION}
    token = ''
    while not token:
        token = input("Please enter your telegram bot token: ")
    config.update({'token': token})

    with open('config.json', 'w') as f:
        f.write(json.dumps(config, sort_keys=True, indent=4,
                           separators=(',', ': ')))

    return config


if __name__ == '__main__':
    if not HAS_TELEGRAM:
        print('Error: Necessary package python-telegram-bot is missing')
        print('To install: pip3 install python-telegram-bot')
        exit(1)

    # Load config file
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        if 'token' not in config:
            raise ValueError
        if 'version' not in config:
            raise ValueError

    except FileNotFoundError:
        # Generate config file
        config = generate_config()
    except ValueError:
        print('Error: Invalid config file.')
        exit(1)

    # Initialize logging
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.ERROR, format=logging_format)

    # Initialize objects
    mokubot = MokuBot(config['token'])
    # Start mokubot in a new thread
    mokubot_t = threading.Thread(target=mokubot.run, daemon=True)
    mokubot_t.start()

    # Start getting commands from the terminal
    command_engine(mokubot)

    # Clear up
    mokubot_t.join()
    exit(0)
