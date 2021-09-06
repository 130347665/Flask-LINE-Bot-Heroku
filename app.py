import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationSendMessage

app = Flask(__name__)

#line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
#handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
line_bot_api = LineBotApi("93KFpjphfNbia39vCRFHNW3kS1YsdQSbdXGYtBZLzmH2u93GXdahxYWYAX0QfJlNu4r4Dq19s3S9aE5b3RC9MqU7HH4oP4aWWATpaNiapbjC9phVpF20AWthMURSTs5L49WMA/h1hp4XKleQYt7zRQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("d5d91f7c24792885fc48d6eb3675dd29")
def filter_bigger_12string(string):
    if len(string) <=12 and len(string)>3:
        return True
    else:
        False


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    new_get_message = ""
    #Send To Line
    if "捷達" in get_message:
        reply= LocationSendMessage(
            type= "location",
            title= "捷達貨運有限公司",
            address= "338桃園市蘆竹區海山路一段340號",
            latitude= 25.097043,
            longitude= 121.26368
        )
    if "誰是捷達最帥的人" == get_message:
        reply = TextSendMessage(text=f"胡紹安")

    #reply = TextSendMessage(text=f"{get_message}")
    if "改錯單" in get_message:
        get_message = get_message.split()
        get_message = filter(filter_bigger_12string,get_message)
        for i in get_message:
            new_get_message += i[0:8] + "\n"
        reply = TextSendMessage(text=f"{new_get_message}")
    if "林雨聖" or "Charles" in get_message:
        reply = TextSendMessage(text=f"AV帝王")
        print(get_message)
    line_bot_api.reply_message(event.reply_token, reply)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)