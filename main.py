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
import config, lineapphandl, richmenu
import os


app = Flask(__name__)

YOUR_CHANNEL_SECRET = config.YOUR_CHANNEL_SECRET
YOUR_CHANNEL_ACCESS_TOKEN = config.YOUR_CHANNEL_ACCESS_TOKEN

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# check for existing richmenu
rich_menu_list = line_bot_api.get_rich_menu_list()
if not rich_menu_list:
    result = richmenu.createRichmeu()
    if not result:
        reply.reply_message(event, config.FAILED)

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
    lineapphandl.TextMessage(event)

if __name__ == '__main__':
    app.run()