from flask import Flask, request, abort
import os,json,shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scrape_requests import Set


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
    #app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

park = "park"
genre = "genre"
area = "area"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global park,genre,area
    park = "park"
    genre = "genre"
    area = "area"

    text = event.message.text


    #最初とリセット時
    if text == "待ち時間":
        les = "les"
        template = template_env.get_template('theme_select.json')
        data = template.render(dict(items=les))

        line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="テーマ選択",
            contents=BubbleContainer.new_from_json_dict(json.loads(data))
            )
        )
    
    else:
        #リッチメニューが選択されたとき
        richmenu_list = ["アトラクション","パレード/ショー","グリーティング","レストラン","ガイドツアー","FP"]

        for richmenu in richmenu_list:
            if text == richmenu:
                genre = text
    


@handler.add(PostbackEvent)
def handle_postback(event):
    global park,genre,area
    area = ""

    post_data = event.postback.data
    userid = event.source.user_id

    land_area_list = ["ワールドバザール","アドベンチャーランド","ウエスタンランド","クリッターカントリー","トゥーンタウン","トゥモローランド"]
    sea_area_list = ["メディテレニアンハーバー","アメリカンウォーターフロント","ポートディスカバリー","ロストリバーデルタ","アラビアンコースト","マーメイドラグーン","ミステリアスアイランド"]

    if post_data == "land" or post_data == "sea":
        park = post_data

        #ランドを選択したときのカルーセル表示
        if park == "land":
            les = "les"
            template = template_env.get_template('land_theme.json')
            data = template.render(dict(items=les))

            land_carousel = FlexSendMessage(
                alt_text="テーマランド",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
                )
            line_bot_api.push_message(userid, messages=land_carousel)

        #シーを選択したときのカルーセル表示
        if park == "sea":
            les = "les"
            template = template_env.get_template('sea_theme.json')
            data = template.render(dict(items=les))

            sea_carousel = FlexSendMessage(
                alt_text="テーマポート",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
                )
            line_bot_api.push_message(userid, messages=sea_carousel)
    
    if park == "land":
        for area in land_area_list:
            print("ここまで来てる")
            print(area)
            if post_data == area:
                area = post_data
                print("ランド")
                #ポストバック受け取り確認
                confirm_message = TextSendMessage(text="処理中です")
                line_bot_api.push_message(userid, messages=confirm_message)
    
    elif park == "sea":
        for area in sea_area_list:
            print("ここまで来てる")
            if post_data == area:
                area = post_data
                print("シー")
                #ポストバック受け取り確認
                confirm_message = TextSendMessage(text="処理中です")
                line_bot_api.push_message(userid, messages=confirm_message)

    #開閉園、スクレイピング、レシート作成
    situation = Set(park,area)

    if situation == "open":
        print("open")

        #レシート出力
        les = "les"
        template = template_env.get_template('recipt.json')
        data = template.render(dict(items=les))

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