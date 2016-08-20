# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import urlfetch

app = Flask(__name__)

access_token = 'EAAZASwfVcXg8BALe8TFMKH7PGtsUBzSZApZA1FCenZA2OSk6M0SuEFG01PRkrTPe76tccCUGMsJgXLcLRMlcPl93qaqZChXi0ZCx0G1T97PXjoChzcbm6uhfCEvARJUsHZAhOEmnaZAQjqP99exMxNVzRuiasiPPoGJXfopgprByEgZDZD'


@app.route("/", methods=["GET"])
def root():
    return "Hello World!"


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
        abort(400)

    return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.json

    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']
                        reply(sender_id, message_text)

    return "ok", 200

def reply(recipient_id, message_text):
    params = {
        "access_token": access_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

def rules(recipient_id, message_text):
    rules = {
        "Hello": "World",
        "Foo": "Bar"
    }

    if message_text in rules:
        reply(recipient_id, rules[message_text])

    else:
        reply(recipient_id, "You have to write something I understand ;)")    

    print data

    url = "https://graph.facebook.com/v2.6/me/messages?" + urllib.urlencode(params)
    r = urlfetch.fetch(url=url, headers=headers, method='POST', payload=data)
