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
    MessageEvent, TextMessage, PostbackTemplateAction, PostbackEvent, PostbackAction, QuickReplyButton, QuickReply,
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
info_url = ""
target_url = ""
counter = 0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global park,genre,area,info_url,target_url,counter

    text = event.message.text
    userid = event.source.user_id
    print(text)

    #最初とリセット時
    if text == "ホーム":
        #初期化
        park = "park"
        genre = "genre"
        area = "area"
        info_url = ""
        target_url = ""
        counter = 0


        les = "les"
        template = template_env.get_template('theme_select.json')
        data = template.render(dict(items=les))


        select__theme_massage = FlexSendMessage(
                alt_text="テーマ選択",
                contents=BubbleContainer.new_from_json_dict(json.loads(data))
                )
            
        line_bot_api.push_message(userid, messages=select__theme_massage)   
    
    else:
        #リッチメニューが選択されたとき
        richmenu_list = ["アトラクション","パレード/ショー","グリーティング","レストラン","ガイドツアー","FP"]

        for richmenu in richmenu_list:
            if text == richmenu:
                genre = text
                print(genre)
                
                if genre == "アトラクション":
                    #quickreplyはjsonで書くこともできる（下記サイト）
                    #https://developers.line.biz/ja/docs/messaging-api/using-quick-reply/
                    select_list = ["待ち時間TOP10","エリア別"]
                    items = [QuickReplyButton(action=PostbackAction(label=f"{select}",data = f"{select}")) for select in select_list]
                    
                    quick_messages = TextSendMessage(text="どちらで表示しますか？",
                                quick_reply=QuickReply(items=items))

                    line_bot_api.push_message(userid, messages=quick_messages)

        if park == "land" and genre != "アトラクション":
            if genre == "パレード/ショー":
                target_url = "https://tokyodisneyresort.info/showSchedule.php?park=land"
            
            elif genre == "グリーティング":
                target_url = "https://tokyodisneyresort.info/greeting_realtime.php?park=land"
            
            elif genre == "レストラン":
                target_url = "https://tokyodisneyresort.info/restwait.php?park=land"
            
            elif genre == "ガイドツアー":
                target_url = "https://tokyodisneyresort.info/guideRealtime.php?park=land"
            
            elif genre == "FP":
                target_url = "https://tokyodisneyresort.info/fastpass.php?park=land"
                    

        elif park == "sea" and genre != "アトラクション":

            if genre == "パレード/ショー":
                target_url = "https://tokyodisneyresort.info/showSchedule.php?park=sea"
            
            elif genre == "グリーティング":
                target_url = "https://tokyodisneyresort.info/greeting_realtime.php?park=sea"
            
            elif genre == "レストラン":
                target_url = "https://tokyodisneyresort.info/restwait.php?park=sea"
            
            elif genre == "ガイドツアー":
                target_url = "https://tokyodisneyresort.info/guideRealtime.php?park=sea"
            
            elif genre == "FP":
                target_url = "https://tokyodisneyresort.info/fastpass.php?park=sea"


        if info_url != "" and target_url != "":
            #ポストバック受け取り確認
            confirm_message = TextSendMessage(text="処理中です")
            line_bot_api.push_message(userid, messages=confirm_message)

            #開閉園、スクレイピング、レシート作成
            situation = Set(park,area,info_url,target_url,genre)

        #テスト用!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
        situation = "open"

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

        elif situation == "close":
            print("close")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="閉園中です")
                )

@handler.add(PostbackEvent)
def handle_postback(event):
    global park,genre,area,info_url,target_url,counter
    area = ""

    post_data = event.postback.data
    userid = event.source.user_id

    if post_data == "エリア別" or post_data == "待ち時間TOP10":
        genre = post_data

    land_area_list = ["ワールドバザール","アドベンチャーランド","ウエスタンランド","クリッターカントリー","トゥーンタウン","トゥモローランド"]
    sea_area_list = ["メディテレニアンハーバー","アメリカンウォーターフロント","ポートディスカバリー","ロストリバーデルタ","アラビアンコースト","マーメイドラグーン","ミステリアスアイランド"]

    print("park = " + str(park))
    print("genre = " + str(genre))
    

    if post_data == "land" or post_data == "sea":
        park = post_data
        if park == "land":
            #開園時間や天気などのリンク
            info_url = "https://tokyodisneyresort.info/index.php?park=land"
            park_ja = "ランド"
        
        elif park == "sea":
            #開園時間や天気などのリンク
            info_url = "https://tokyodisneyresort.info/index.php?park=sea"
            park_ja ="シー"

        park_message = TextSendMessage(text= str(park_ja) + "を選択しています\nカテゴリを下のメニューから\n選択してください")
        line_bot_api.push_message(userid, messages=park_message)

    #ランドを選択したときのカルーセル表示
    if park == "land" and genre == "エリア別":
        counter += 1

        if counter == 1:
            les = "les"
            template = template_env.get_template('land_theme.json')
            data = template.render(dict(items=les))

            land_carousel = FlexSendMessage(
                alt_text="テーマランド",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
                )
            line_bot_api.push_message(userid, messages=land_carousel)
        

    #シーを選択したときのカルーセル表示
    elif park == "sea" and genre == "エリア別":
        counter += 1

        if counter == 1:
            les = "les"
            template = template_env.get_template('sea_theme.json')
            data = template.render(dict(items=les))

            sea_carousel = FlexSendMessage(
                alt_text="テーマポート",
                contents=CarouselContainer.new_from_json_dict(json.loads(data))
                )
            line_bot_api.push_message(userid, messages=sea_carousel)
            
    #カルーセルのボタンが押された後の処理
    if park == "land" and genre == "エリア別":
        for land_area in land_area_list:
            if post_data == land_area:
                area = post_data

                #リッチメニューによるURLの変化
                if genre == "エリア別":
                    target_url = "https://tokyodisneyresort.info/realtime.php?park=land&order=area_name" 
                


    #ランドでアトラクション以外が選択されたとき
    if park == "land" and genre != "エリア別":
        if genre == "待ち時間TOP10":
            target_url = "https://tokyodisneyresort.info/realtime.php?park=land&order=wait"

    #カルーセルのボタンが押された後の処理
    elif park == "sea" and genre == "エリア別":
        for sea_area in sea_area_list:
            if post_data == sea_area:
                area = post_data
                
                #リッチメニューによるURLの変化
                if genre == "エリア別":
                    target_url = "https://tokyodisneyresort.info/realtime.php?park=sea&order=area_name"

               

    if park == "sea" and genre != "エリア別":
        #リッチメニューによるURLの変化
        if genre == "待ち時間TOP10":
            target_url = "https://tokyodisneyresort.info/realtime.php?park=sea&order=wait" 



    
    if info_url != "" and target_url != "":
        #ポストバック受け取り確認
        confirm_message = TextSendMessage(text="処理中です")
        line_bot_api.push_message(userid, messages=confirm_message)

        print("target = " + str(target_url))
        #開閉園、スクレイピング、レシート作成
        situation = Set(park,area,info_url,target_url,genre)
    
    else:
        situation = ""

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

    elif situation == "close":
        print("close")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="閉園中です")
            )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)