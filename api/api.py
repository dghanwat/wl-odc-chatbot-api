from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
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
            "WL ODC is a great place to work",
            "What is SPARK",
            "SPARK is WL ODC platform to develop innovative ideas",
            "What is WIN",
            "WIN Stands for Worldline Innovative Network."
        ]
        chatBot.set_trainer(ChatterBotCorpusTrainer)
        chatBot.set_trainer(ListTrainer)
        chatBot.train(
            "chatterbot.corpus.english"
        )
        chatBot.train(conversation)
        return {'result': 'Agent training completed successfully'}


class ChatBotQuestions(Resource):
    def get(self):
        #         Get the existing set of questions from Firebase
        return jsonify(result="")

    def post(self):
        jsonData = request.get_json(force=True)
        senderId = jsonData['senderId']
        question = jsonData['question']
        answer = jsonData['answer']
        tenantId = jsonData['tenantId']
        return jsonify(result="")


class ChatBot(Resource):

    def post(self):
        jsonData = request.get_json(force=True)
        senderId = jsonData['senderId']
        query = jsonData['query']

        response = str(chatBot.get_response(query))
        return jsonify(result=response)


api.add_resource(HelloWorld, '/')
api.add_resource(ChatBotTrain, '/chat/train')
api.add_resource(ChatBot,
                 '/chat')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)