import os,sys
import random
from flask import Flask, request
from pymessenger.bot import Bot
from fbmq import Page
import datetime
import sqlite3
from sqlite3 import Error
from difflib import SequenceMatcher
import difflib
countt = 0
docID = 0
patID = 0
all_ids_have_initial_message = []
allSymptoms = []
initialSymptoms = []

app = Flask(__name__)

ACCESS_TOKEN = os.environ["access"]
# This is API key for facebook messenger.
API = "https://graph.facebook.com/v13.0/me/messages?access_token="+ACCESS_TOKEN
VERIFY_TOKEN = 'test'
# bot=Bot(ACCESS_TOKEN)


# @app.route("/", methods=['GET', 'POST'])
# def receive_message():
#     if request.method == 'GET':
#         """Before allowing people to message your bot, Facebook has implemented a verify token
#         that confirms all requests that your bot receives came from Facebook."""
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     # if the request was not get, it must be POST and we can just proceed with sending a message back to user
#     else:
#         # get whatever message a user sent the bot
#         output = request.get_json()
#         for event in output['entry']:
#             messaging = event['messaging']
#             for message in messaging:
#                 if message.get('message'):
#                     # Facebook Messenger ID for user so we know where to send response back to
#                     recipient_id = message['sender']['id']
#                     timeee = str(datetime.datetime.today().strftime('%Y-%m-%d'))
#                     if message['message'].get('text'):
#                         firstText = message['message'].get('text')  # get_message()
#                         user_name = ""
#                         doctorsList = []
#                         patientList = []
#                         if not message['message'].get('is_echo'):
#                             user_profile = page.get_user_profile(recipient_id)
#                             user_name = user_profile['first_name']
#
#                             response_sent_text = ""
#                             conn = sqlite3.connect('all-data-shaksny.db')
#                             cur1 = conn.execute("SELECT id from user")
#                             patientList = cur1.fetchall()
#                             conn.commit()
#                             cur2 = conn.execute("SELECT id from doctor")
#                             doctorsList = cur2.fetchall()
#
#                             conn.commit()
#                             docList = []
#                             for item in doctorsList:
#                                 docList.append(item[0])
#                             patList = []
#                             for item in patientList:
#                                 patList.append(item[0])
#
#                             if countt == 0:
#                                 if (recipient_id not in patList) and (recipient_id not in docList):
#                                     global all_ids_have_initial_message
#                                     if (recipient_id not in all_ids_have_initial_message):
#                                         all_ids_have_initial_message.append(recipient_id)
#                                         send_message(recipient_id,
#                                                      "Hey <3 .. Please tell me, are you patient or doctor ? ")
#                                     if "patient" in firstText or "Patient" in firstText or "PATIENT" in firstText:
#                                         cur3 = conn.execute(
#                                             "INSERT INTO user (id, date, mess, conversation) VALUES (?,?,?,?)",
#                                             (recipient_id, timeee, firstText, "unfinished"))
#                                         conn.commit()
#                                         send_message(recipient_id, "welcome " + user_name + " <3 ")
#                                         send_message(recipient_id,
#                                                      "Please describe what do you feel in detail to help you ^_^ ")
#                                     elif "doctor" in firstText or "Doctor" in firstText or "DOCTOR" in firstText or "DR" in firstText or "Dr" in firstText or "dr" in firstText:
#                                         cur4 = conn.execute("INSERT INTO doctor (id, specialty ) VALUES (?,?)",
#                                                             (recipient_id, "None"))
#                                         conn.commit()
#                                         send_message(recipient_id, "welcome Dr " + user_name + " <3 ")
#                                         send_message(recipient_id,
#                                                      "Shakhsny Bot family happy for joining you with us to help patients <3  we will send messages to you when patient need to communicate with you  ^_^ ")
#
#                                 else:
#                                     if recipient_id in patList:
#                                         flag = False
#                                         countP = 0
#                                         for item in patList:
#                                             if recipient_id == item:
#                                                 countP += 1
#                                         if countP > 0:
#                                             cur5 = conn.execute(
#                                                 "SELECT conversation from user where id=" + recipient_id)
#                                             conn.commit()
#                                             for item in cur5:
#                                                 if item[0] == "unfinished":
#                                                     flag = True
#                                             if flag == True:
#                                                 cur7 = conn.execute(
#                                                     "SELECT mess from user where id=" + recipient_id + " and conversation='unfinished'")
#                                                 messages = ""
#                                                 for rows in cur7:
#                                                     messages += rows[0]
#                                                 messages += "," + firstText
#                                                 conn.execute("UPDATE user set mess= ? where id= ? and conversation= ?",
#                                                              (messages, recipient_id, 'unfinished'))
#                                                 conn.commit()
#                                             else:
#                                                 cur6 = conn.execute(
#                                                     "INSERT INTO user (id, date, mess, conversation) VALUES (?,?,?,?)",
#                                                     (recipient_id, timeee, firstText, "unfinished"))
#                                                 conn.commit()
#
#                             cur8 = conn.execute(
#                                 "SELECT mess from user where id=" + recipient_id + " and conversation='unfinished'")
#                             for item in cur8:
#                                 response_sent_text += item[0]
#                             conn.commit()
#                             conn.close()
#                             all_conversation(response_sent_text, firstText, patList, docList, recipient_id, user_name)
#
#                     if message['message'].get('attachments'):
#                         firstText = "No text"  # get_message()
#                         send_message(recipient_id, firstText)
#
#     return "Message Processed"


# host = os.environ.get("IP", "0.0.0.0")
# port = int(os.environ.get("PORT", 8000))
# app.run(host=host, port=port)



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