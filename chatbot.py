from chatterbot import ChatBot

class Chat():
    def __init__(self, botname):
        # Initialize chatbot
        self.bot = ChatBot(
            botname,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database='./db.sqlite3',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                },
                {
                    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                    'threshold': 0.3,
                    'default_response': 'I\'m sorry, but I do not understand'
                }
            ],
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )

        self.bot.train('chatterbot.corpus.english')

    def get_response(self, user_input):
        return self.bot.get_response(user_input).text
