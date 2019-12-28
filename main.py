from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,TextMessage,TextSendMessage,ConfirmTemplate,MessageAction,TemplateSendMessage,QuickReplyButton,QuickReply,RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds,URIAction
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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

def response_message(event):
    language_list = ["Ruby", "Python", "PHP", "Java", "C"]

    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}が好き")) for language in language_list]

    messages = TextSendMessage(text="どの言語が好きですか？",
                            quick_reply=QuickReply(items=items))

    line_bot_api.reply_message(event.reply_token, messages=messages)

def createRichmenu(event):
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="Tap here",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
            action=URIAction(label='Go to line.me', uri='https://line.me'))]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

    image = 'tdl-wb.jpg'
    path = '/photo/'+image 

    with open(path, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)

    line_bot_api.set_default_rich_menu(rich_menu_id)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
    
    text=event.message.text
    if text == 'land':
        confirm_template = ConfirmTemplate(text='エリアを選択してください', actions=[
            MessageAction(label='ワールドバザール', text='ワールドバザール'),
            MessageAction(label='アドベンチャー', text='アドベンチャー'),
            MessageAction(label='ウエスタン', text='ウエスタン'),
            MessageAction(label='クリッター', text='クリッター'),
            MessageAction(label='ファンタジー', text='ファンタジー'),
            MessageAction(label='トゥーン', text='トゥーン'),
            MessageAction(label='トゥモロー', text='トゥモロー'),

        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'い':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    elif text == 'う':
        response_message(event)
    else:
        createRichmenu(event)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)