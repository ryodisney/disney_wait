from flask import Flask, request, abort
import os,json
from jinja2 import Environment, FileSystemLoader, select_autoescape

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage,
    FlexSendMessage, BubbleContainer, CarouselContainer, TextSendMessage
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

template_env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml', 'json'])
)

@app.route("/")
def hello_world():
    return "hello world!"

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
        abort(400)

    return 'OK'

"""
基本的にはここから下が
"""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
    
    text=event.message.text
    data = event.postback.data
    #確認ボタンは二つしか無理
    if text == 'land':
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="ここまできてる")
        )
        les = "les"
        template = template_env.get_template('button_temp.json')
        data = template.render(dict(items=les))
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="items",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
            )
        )

        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=data)
        )

    elif text == 'sea':
        les = "les"
        template = template_env.get_template('sea_theme.json')
        data = template.render(dict(items=les))
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="items",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
            )
        )
        


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)