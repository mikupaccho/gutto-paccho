# -*- coding: utf-8 -*-
import random
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

STATUS = {
    'is_attendance': False,
    'attendance_list': []
}

LIMIT_MEMBER_COUNT = 6



@respond_to('メンション')
def mention_func(message):
    message.reply('私にメンションと言ってどうするのだ') # メンション
    send_user = message.channel._client.users[message.body['user']][u'name']
    print(send_user)
    message_text=message.body['text']
    print(message_text)


@listen_to('.+')
def listen_func(message):
    send_user = message.channel._client.users[message.body['user']][u'name']
    message_text=message.body['text']
    if STATUS['is_attendance']:
        print(send_user,message_text)
        if message_text in ['はい']:
            STATUS['attendance_list'].append(send_user)

@respond_to('募集')
def start(message):
    message.send('募集を開始します')
    STATUS['is_attendance'] = True

@respond_to('終了')
def start(message):
    message.send('募集を終了します')
    STATUS['is_attendance'] = False
    print(STATUS['attendance_list'])
    attendance_list = list(set(STATUS['attendance_list']))
    if len(attendance_list) >= LIMIT_MEMBER_COUNT:
        random.shuffle(attendance_list)
        member_count = len(attendance_list)//2
        message.send(','.join(attendance_list[:member_count]))
        message.send(','.join(attendance_list[member_count:]))
    else:
        message.send(','.join(attendance_list))
    STATUS['attendance_list'] = []
