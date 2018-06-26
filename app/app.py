from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pyrebase

config = {}
config['apiKey'] = "AIzaSyBmc7ZDPODEoYMjskk-TZMm1fGUuARtpnY"
config['authDomain'] = "wl-odc-chatbot.firebaseapp.com"
config['databaseURL'] = "https://wl-odc-chatbot.firebaseio.com"
config['projectId'] = "wl-odc-chatbot"
config['storageBucket'] = "wl-odc-chatbot.appspot.com"

firebase = pyrebase.initialize_app(config)
db = firebase.database()
app = Flask(__name__)
api = Api(app)
chatBot = ChatBot("WL ODC")

class QnA(object):
    """__init__() functions as the class constructor"""
    def __init__(self, question=None, answer=None, createdBy=None):
        self.question = question
        self.answer = answer
        self.createdBy = createdBy

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
        allQnAs = []
        all_data = db.child("training-data").get()
        for qna in all_data.each():
            allQnAs.append(qna.val())
        return jsonify(result=allQnAs)

    def post(self):
        jsonData = request.get_json(force=True)
        senderId = jsonData['senderId']
        question = jsonData['question']
        answer = jsonData['answer']
        tenantId = jsonData['tenantId']

        data = {
            "question": question,
            "answer": answer,
            "createdBy": senderId
        }
        db.child("training-data").push(data)
        return {'result': 'QnA saved successfully'}


class ChatBot(Resource):

    def post(self):
        jsonData = request.get_json(force=True)
        senderId = jsonData['senderId']
        query = jsonData['query']

        response = str(chatBot.get_response(query))
        return jsonify(result=response)


api.add_resource(ChatBotTrain, '/api/chat/train')
api.add_resource(ChatBot, '/api/chat')
api.add_resource(ChatBotQuestions, '/api/chat/qna');


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
