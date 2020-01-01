from flask import Flask, request, abort
import os,json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scrape import Set
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, PostbackTemplateAction, PostbackEvent,
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



park = "park"
area = "area"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global park
    park = event.message.text

    if park == "land":
        les = "les"
        template = template_env.get_template('land_theme.json')
        data = template.render(dict(items=les))

        line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="items",
            contents=CarouselContainer.new_from_json_dict(json.loads(data))
            )
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    print("ここまで来てる")
    global park,area    
    area = event.postback.data

    #開閉園、スクレイピング、レシート作成
    situation = Set(park,area)
    print(situation)

    if situation == "open":
        print("open")
        #レシート出力
        les = "les"
        template = template_env.get_template('recipt.json')
        data = template.render(dict(items=les))
        print(data)

        line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="items",
            contents=BubbleContainer.new_from_json_dict(json.loads(data))
            )
        )
    
    else:
        print("close")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="閉園中です")
            )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)