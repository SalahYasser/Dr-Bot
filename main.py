from flask import Flask, request
import os
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ["access"]
# This is API key for facebook messenger.
API = "https://graph.facebook.com/v13.0/me/messages?access_token="+PAGE_ACCESS_TOKEN
VERIFY_TOKEN = 'test'

@app.route("/", methods=['GET'])
def fbverify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    print(data)
    # Read messages from facebook messanger.
    message = data['entry'][0]['messaging'][0]['message']['text']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    #print(message['text'])
    # if(message['text'] == 'hi'):
    request_body = {
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "Please wait, we will reply to you as soon as possible"
        }
    }
    response = requests.post(API, json=request_body).json()
    return response


host = os.environ.get("IP", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))
app.run(host=host, port=port)

# @app.route("/ping", methods=['GET'])
# def ping():
#     return "pong", 200



# @app.route("/", methods=['POST'])
# def fbwebhook():
#     data = request.get_json()
#     print(data)
#     try:
#         # Read messages from facebook messanger.
#         message = data['entry'][0]['messaging'][0]['message']
#         sender_id = data['entry'][0]['messaging'][0]['sender']['id']
#
#         request_body = {
#             "recipient": {
#                 "id": sender_id
#             },
#             "message": {
#                 "text": "hello, world!"
#             }
#         }
#
#         # if message['text'] == "hi":
#         response = requests.post(API, json=request_body).json()
#         return response
    # else:
    #     response = requests.post(API, json=request_body).json()
    #     return response

    # except:
    # # Here we are store the file to our server who send by user from facebook messanger.
    #     try:
    #         mess = data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url']
    #         print("for url-->", mess)
    #         json_path = requests.get(mess)
    #         filename = mess.split('?')[0].split('/')[-1]
    #         open(filename, 'wb').write(json_path.content)
    #     except:
    #         print("Not Found-->")
    #
    #
    # return 'ok'


