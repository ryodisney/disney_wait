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
import config, reply
import random, copy

YOUR_CHANNEL_SECRET = config.YOUR_CHANNEL_SECRET
YOUR_CHANNEL_ACCESS_TOKEN = config.YOUR_CHANNEL_ACCESS_TOKEN

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

usersList = []
usersDic = {}

def TextMessage(event):
    userId = event.source.user_id
    message = event.message.text

    if not userId in usersList:
        usersList.append(userId)
        if not userId in usersDic.keys():
            usersDic[userId] = {}
            usersDic[userId]['toUserId'] = ''

    toUsersList = copy.copy(usersList)
    toUsersList.remove(userId)


    if message == config.NEXT:
        if not len(toUsersList) == 0:
            num = random.randint(0, int(len(toUsersList)-1))
            usersDic[userId] = toUsersList[num]
            toUserId = toUsersList[num]
            usersDic[toUserId] = userId

            # delete Id form list
            usersList.remove(userId)
            usersList.remove(toUserId)

            # reply
            message = TextSendMessage(text=config.MATCHED)
            reply.reply_message(event, message)
            reply.push_message(toUserId, message)

        else:
            message = TextSendMessage(text=config.NOTNEXT)
            reply.reply_message(event, message)

    elif message == config.REMOVE:
        usersList.remove(userId)
        toUserId = usersDic[userId]
        if userId in usersDic.values():
            pushMessage = TextSendMessage(text=config.REMOVED)
            reply.push_message(toUserId, pushMessage)
            usersDic[toUserId] = ''
        usersDic.pop(userId)

        message = TextSendMessage(text=message)
        reply.reply_message(event, message)

    else:
        if usersDic[userId] == '':
            message = TextSendMessage(text=message)
            reply.reply_message(event, message)

        else:
            toUserId = usersDic[userId]
            message = TextSendMessage(text=message)
            reply.push_message(toUserId, message)