from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import sys
import json


class MokuBot():
    def __init__(self, token):
        # Initialize updater
        self.updater = Updater(token)

        # Add command handlers
        hello_handler = CommandHandler('hello', self.hello)
        self.updater.dispatcher.add_handler(hello_handler)
        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.updater.dispatcher.add_handler(unknown_handler)

    def stop(self):
        self.updater.stop()

    def hello(self, bot, update):
        text = 'Hello {}'.format(update.message.from_user.first_name)
        update.message.reply_text(text)

    def unknown(self, bot, update):
        text = 'Sorry, I didn\'t understand that command.'
        update.message.reply_text(text)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    # Load config file
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        if 'token' not in config:
            raise ValueError
        if 'version' not in config:
            raise ValueError

    except FileNotFoundError:
        print('Error: Config file not found.')
        exit(1)
    except ValueError:
        print('Error: Invalid config file.')
        exit(1)


    # initialize objects
    mokubot = MokuBot(config['token'])
    # Start mokubot
    mokubot.run()
