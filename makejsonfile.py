#coding:utf-8
import json

def Make_jsonfile(attraction,info):
    json_file = open('templates/recipt.json', 'r',encoding="utf-8-sig")
    json_object = json.load(json_file)

    new =   {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": str(attraction),
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": str(info[0])+str(info[1]),
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                }
            ]
        }

    json_object["body"]["contents"][3]["contents"].append(new)

    new_json_file = open('templates/recipt.json', 'w',encoding="utf-8-sig")
    json.dump(json_object, new_json_file, indent=2,ensure_ascii=False)

#エリアのみ書き込む
def Send_area(area):
    json_file = open('templates/recipt.json', 'r',encoding="utf-8-sig")
    json_object = json.load(json_file)
    json_object["body"]["contents"][1]["text"] = str(area)
    #書き込み
    new_json_file = open('templates/recipt.json', 'w',encoding="utf-8-sig")
    json.dump(json_object, new_json_file, indent=2,ensure_ascii=False)