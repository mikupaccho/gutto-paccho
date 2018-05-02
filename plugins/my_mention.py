import math
import random
from slackbot.bot import listen_to, respond_to

g_status = {
    'is_open': False,
    'is_silent': False,
    'attendee_list': [],
}

LIMIT_MEMBER_COUNT = 6
KATAKANA = {chr(n) for n in range(ord(str('ァ')), ord(str('ヾ')))} - {'・', 'ヵ', 'ヶ'}
KATAKANA -= {'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ッ', 'ャ', 'ュ', 'ョ', 'ヽ', 'ヾ', 'ヮ', 'ー', 'ン'}
KATAKANA |= {'キャ', 'キュ', 'キョ', 'ギャ', 'ギュ', 'ギョ', 'シャ', 'シュ', 'ショ', 'ジャ', 'ジュ'}
KATAKANA |= {'ジョ', 'ニャ', 'ニュ', 'ニョ', 'ミャ', 'ミュ', 'ミョ', 'ヒャ', 'ヒュ', 'ヒョ', 'チャ'}
KATAKANA |= {'チュ', 'チョ', 'リャ', 'リュ', 'リョ', 'ヴァ', 'ヴィ', 'ヴェ', 'ー', 'ン'}

# YESと判断されるメッセージリスト
YES_MESSAGE_LIST = ['はい', '行きます', 'おなかすいた']


@listen_to('.+')
def listen(message):
    user = message.body.get('user')
    if user:
        send_user = message.channel._client.users[user]['name']
        message_text = message.body['text']
        if g_status['is_open']:
            print(send_user, message_text)
            if message_text in YES_MESSAGE_LIST:
                g_status['attendee_list'].append('<@{}>'.format(send_user))
                message.react('+1')
    else:
        message.send('誰？')


@respond_to('(.+)?募集')
def start(message, how_to):
    start_message = 'はらぺこ軍団全員集合〜「{}」って応答するパッチョ'.format(' か、'.join(YES_MESSAGE_LIST))
    if how_to and '静か' in how_to:
        start_message += '(こっそり)'
        g_status['is_silent'] = True
    else:
        start_message += '<!here>'

    message.send(start_message)
    g_status['is_open'] = True


def _split_attendee_list(attendee_list, limit_member_count):
    """
    Parameters
    ----------
    attendee_list: list[str]
        参加希望者の名前のリスト。
    limit_member_count: int
        各チームの最大人数を表す自然数。

    Returns
    ----------
    各グループに配属された参加者のリストのジェネレータ。
    """
    n_teams = math.ceil(len(attendee_list) / limit_member_count)
    for i_chunk in range(int(n_teams)):
        yield attendee_list[i_chunk * len(attendee_list) // n_teams:(i_chunk + 1) * len(attendee_list) // n_teams]


def _reset_state():
    """
    募集状態のステータスをクリアにする
    :return:
    """
    g_status['is_open'] = False
    g_status['is_silent'] = False
    g_status['attendee_list'] = []


@respond_to('終了')
def end(message):
    end_message = '募集終了だパッチョ '
    if g_status['is_silent']:
        end_message += '(こっそり)'
    else:
        end_message += '<!here>'

    print(g_status['attendee_list'])
    attendee_list = list(set(g_status['attendee_list']))

    # attendee_list をランダムに並び替え
    random.shuffle(attendee_list)

    # メンバー数上限に応じてチームを分割
    splitted_attendee_list = _split_attendee_list(attendee_list, LIMIT_MEMBER_COUNT)

    # 各グループごとに名前をランダム生成してslackに通知
    for attendee_group in splitted_attendee_list:
        team_name = random.sample(KATAKANA, 2)
        message.send('*チーム{}{}パッチョ*'.format(team_name[0], team_name[1]))
        for name in attendee_group:
            message.send(name)
    # 募集状態のリセット
    _reset_state()
