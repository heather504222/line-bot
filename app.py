from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('srxLITwTeS6isNCr68NPdympZEAcJztGHHwQT++i+Qq9UeWJHprz1eXn54SsI2B42YSDW9P5zji1OU+wiCPwb790fw7/lQc6DSYipVZoW3bx3IMFFl+xeRUkq27rtHfR0pvwjgx51OM3F+A6KDiDBAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9cd4ea3df8988e8af375638c6914a1ed')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂你說甚麼'

    if msg in ['hi','Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎?':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg :
        r = '您想訂位嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= r))


if __name__ == "__main__":
    app.run()