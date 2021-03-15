from flask import Blueprint, render_template, url_for, request, session, redirect, flash, current_app, Response
from .extension import mongo, login_required
import os
from bson import ObjectId
import json
from pymessenger.bot import Bot
from pymessenger import Element, Button
bot = Bot("EAAEC05eCRSQBAGDZAjsEZCy8MewS18yiFEhebkqLKAO4s556ZBGtSjJJ6NumYSaX0IfSEtJuzZCUvKZCh6yKxmTE0vSBMZAgjpW1MNY7lGHLmNAZBxs9TLmZCGbap8nvEbZAEGXSdaz6JdTJBzBbyKZChfr5pPEdFmoWAhZCmGqga0WoHaZCsjzmztVK")
VERIFY_TOKEN = "test"

api = Blueprint('api', __name__)

# @api.route('/test',methods=['GET','POST'])
# def test():
#     if request.method == 'GET':
#         if request.args.get("hub.verify_token") == VERIFY_TOKEN:
#             return request.args.get("hub.challenge")
#         else:
#             return 'Invalid verification token'

#     if request.method == 'POST':
#         output = request.get_json()
#         for event in output['entry']:
#             messaging = event['messaging']
#             for x in messaging:
#                 if x.get('message'):
#                     recipient_id = x['sender']['id']
#                     # if x['message'].get('text'):
#                     #     message = x['message']['text']
#                     #     bot.send_text_message(recipient_id, message)
#                     # if x['message'].get('attachments'):
#                     #     for att in x['message'].get('attachments'):
#                     #         bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
#                     image_url = 'https://lh4.googleusercontent.com/-dZ2LhrpNpxs/AAAAAAAAAAI/AAAAAAAA1os/qrf-VeTVJrg/s0-c-k-no-ns/photo.jpg'
#                     elements = []
#                     element = Element({
#                             "title": "test",
#                             "image_url": "https://f.ptcdn.info/266/072/000/qmysgv17vdVsmVcUtTko-o.jpg",
#                             "subtitle": "test",
#                             "default_action": {
#                                 "type": "web_url",
#                                 "url": "https://petersfancybrownhats.com/view?item=103",
#                                 "webview_height_ratio": "tall"
#                                 },
#                             "buttons": [
#                                 {
#                                     "type": "postback",
#                                     "title": "ดูข้อมูล", "payload": "detail&1111"
#                                     },{
#                                         "type": "postback",
#                                         "title": "ใส่รถเข็น",
#                                         "payload": "cart&1111"
#                                         }
#                                 ]
#                         })
#                     elements.append(element)
#                     result = bot.send_generic_message(recipient_id, elements)
#                 else:
#                     pass
#         return "Success"


@api.route('/', methods=['GET'])
def webhook():
    print(request.args.get('input1'))
    print(request.args.get('p_image_url'))
    return {"message": "hello", "input1": request.args.get('input1')}


@api.route('/receipt', methods=['GET'])
def get_payment():
    transaction_collection = mongo.db.transactions
    transaction_collection.insert({})
    return {"message": "ยืนยันการซื้อเรียบร้อยครับ"}


@api.route('/getlink', methods=['GET', 'POST'])
def get_link():
    if request.method == 'GET':
        return {"message": "success"}
    elif request.method == 'POST':

        return {"message": group_url}


@api.route('/getconcert', methods=['GET'])
def get_concert():
    concert_collection = mongo.db.concerts
    query = request.args.get("query")
    if query is None:
        concert_list = concert_collection.find({"status": "open"}).limit(10)
    else:
        concert_list = concert_collection.find({"$and": [{"status": "open"}, {'title': {'$regex': query, "$options": 'i'}}]}).limit(10)
    concert_list = list(concert_list)
    if len(concert_list) == 0:
        resp = Response('''{
            "line_payload":[
                {
                    "type": "text",
                    "text": "ขอโทษครับ ตอนนี้ไม่มีคอนเสิร์ตที่เปิดให้จอง โปรดลองใหม่อีกครั้งนะครับ"
                }
            ],
            "facebook_payload":[
                {
                    "text": "ขอโทษครับ ตอนนี้ไม่มีคอนเสิร์ตที่เปิดให้จอง โปรดลองใหม่อีกครั้งนะครับ"
                }
            ]
        }''')
        resp.headers['Response-Type'] = 'object'
        return resp
    template = """"""
    for concert in concert_list:
        if template == "":
            template = """{
                "title": "%s", 
                "image_url": "%s", 
                "subtitle": "%s", 
                "default_action": {
                    "type": "web_url", 
                    "url": "https://petersfancybrownhats.com/view?item=103", 
                    "webview_height_ratio": "tall"}, 
                    "buttons": [{
                        "type": "postback", 
                        "title": "ดูข้อมูล", 
                        "payload": "detail&1111"
                        }, {
                            "type": "postback", 
                            "title": "ใส่รถเข็น", 
                            "payload": 
                            "cart&1111"
                            }
                        ]
                }"""%(concert['title'],"https://2946cb768351.ngrok.io/images/concert/"+ concert['image'] ,concert['info'])
        else:
            template = template + "," + """{
                                    "title": "test", 
                                    "image_url": "https://f.ptcdn.info/266/072/000/qmysgv17vdVsmVcUtTko-o.jpg", 
                                    "subtitle": "test", 
                                    "default_action": {
                                        "type": "web_url", 
                                        "url": "https://petersfancybrownhats.com/view?item=103", 
                                        "webview_height_ratio": "tall"}, 
                                        "buttons": [{
                                            "type": "postback", 
                                            "title": "ดูข้อมูล", 
                                            "payload": "detail&1111"
                                            }, {
                                                "type": "postback", 
                                                "title": "ใส่รถเข็น", 
                                                "payload": 
                                                "cart&1111"
                                        }
                                    ]
                                }"""
    resp = Response(
        '''{
            "line_payload":[
                {
                    "type": "text",
                    "text": "Feature นี้สำหรับ facebook เท่านั้น"
                }
            ],
            "facebook_payload":[
                {
                    "attachment": {
                        "type": "template", 
                        "payload": {
                            "template_type": "generic", 
                            "elements": [
                                %s
                            ]
                        }
                    }
                }
            ]
        }'''%(template)
    )
    resp.headers['Response-Type'] = 'object'
    return resp
