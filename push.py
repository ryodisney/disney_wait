from linebot import LineBotApi
from linebot.models import TextSendMessage,  FlexSendMessage
import os

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

payload = {
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "Brown Cafe",
          "size": "xl",
          "weight": "bold"
        },
        {
          "type": "box",
          "layout": "baseline",
          "margin": "md",
          "contents": [
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
              "size": "sm"
            },
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
              "size": "sm"
            },
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
              "size": "sm"
            },
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
              "size": "sm"
            },
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
              "size": "sm"
            },
            {
              "type": "text",
              "text": "4.0",
              "flex": 0,
              "margin": "md",
              "size": "sm",
              "color": "#999999"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "margin": "lg",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "Place",
                  "flex": 1,
                  "size": "sm",
                  "color": "#AAAAAA"
                },
                {
                  "type": "text",
                  "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                  "flex": 5,
                  "size": "sm",
                  "color": "#666666",
                  "wrap": True
                }
              ]
            },
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "Time",
                  "flex": 1,
                  "size": "sm",
                  "color": "#AAAAAA"
                },
                {
                  "type": "text",
                  "text": "10:00 - 23:00",
                  "flex": 5,
                  "size": "sm",
                  "color": "#666666",
                  "wrap": True
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "flex": 0,
      "spacing": "sm",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "CALL",
            "uri": "https://linecorp.com"
          },
          "height": "sm",
          "style": "link"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "WEBSITE",
            "uri": "https://linecorp.com"
          },
          "height": "sm",
          "style": "link"
        },
        {
          "type": "spacer",
          "size": "sm"
        }
      ]
    }
  }
}

container_obj = FlexSendMessage.new_from_json_dict(payload)

line_bot_api.push_message('送りたい相手のUserID', messages=container_obj)