import sys
import json
import threading

try:
    from telegram.ext import Updater, CommandHandler
    HAS_TELEGRAM = True
except ImportError:
    HAS_TELEGRAM = False


class MokuBot():
    def __init__(self, token):
        self.updater = Updater(config['token'])
        self.updater.dispatcher.add_handler(CommandHandler('hello', self.hello))

    def hello(self, bot, update):
        text = 'Hello {}'.format(update.message.from_user.first_name)
        update.message.reply_text(text)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

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
        print('Error: Config file not found.')
        exit(1)
    except ValueError:
        print('Error: Invalid config file.')
        exit(1)

    mokubot = MokuBot(config['token'])
    mokubot_t = threading.Thread(target=mokubot.run, daemon=True)
    # Start the mokubot thread
    mokubot_t.start()
