import random
from slackbot.bot import listen_to, respond_to

g_status = {
    'is_open': False,
    'attendee_list': [],
}

LIMIT_MEMBER_COUNT = 7


@listen_to('.+')
def listen(message):
    send_user = message.channel._client.users[message.body['user']]['name']
    message_text = message.body['text']
    if g_status['is_open']:
        print(send_user, message_text)
        if message_text in ['はい', '行きます', 'おなかすいた']:
            g_status['attendee_list'].append('<@{}>'.format(send_user))


@respond_to('募集')
def start(message):
    message.send('募集を開始します')
    g_status['is_open'] = True


@respond_to('終了')
def end(message):
    message.send('募集を終了します')
    g_status['is_open'] = False
    print(g_status['attendee_list'])
    attendee_list = list(set(g_status['attendee_list']))
    if len(attendee_list) >= LIMIT_MEMBER_COUNT:
        random.shuffle(attendee_list)
        member_count = len(attendee_list) // 2
        message.send('*チームガスパッチョ*')
        for name in attendee_list[:member_count]:
            message.send(name)
        message.send('*チームデンパッチョ*')
        for name in attendee_list[member_count:]:
            message.send(name)

    else:
        message.send('*チームガスパッチョ*')
        for name in attendee_list:
            message.send(name)
    g_status['attendee_list'] = []
