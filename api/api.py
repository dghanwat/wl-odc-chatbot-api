from flask import Flask
from flask_restful import Resource, Api
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
api = Api(app)
chatBot = ChatBot("WL ODC")


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class ChatBotTrain(Resource):
    def post(self):
        conversation = [
            "Hello",
            "Hi there!",
            "How are you doing?",
            "I'm doing great.",
            "That is good to hear",
            "Thank you.",
            "You're welcome.",
            "What is WL ODC",
            "WL ODC is a great place to work"
        ]
        chatBot.set_trainer(ChatterBotCorpusTrainer)
        chatBot.set_trainer(ListTrainer)
        chatBot.train(
            "chatterbot.corpus.english"
        )
        chatBot.train(conversation)
        return {'response': 'Agent training completed successfully'}


class ChatBot(Resource):

    def get(self):
        response = str(chatBot.get_response("What is WL ODC"))

        print("Response from Bot is ", str(response))
        return {'response': response}


api.add_resource(HelloWorld, '/')
api.add_resource(ChatBotTrain, '/chat/train')
api.add_resource(ChatBot,
                 '/chat')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
