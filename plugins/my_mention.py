import math
import random
from slackbot.bot import listen_to, respond_to

g_status = {
    'is_open': False,
    'attendee_list': [],
}

LIMIT_MEMBER_COUNT = 6
KATAKANA = {chr(n) for n in range(ord(str('ァ')), ord(str('ヾ')))} - {'・', 'ヵ', 'ヶ'}
KATAKANA -= {'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ッ', 'ャ', 'ュ', 'ョ', 'ヽ', 'ヾ', 'ヮ', 'ー', 'ン'}
KATAKANA |= {'キャ', 'キュ', 'キョ', 'ギャ', 'ギュ', 'ギョ', 'シャ', 'シュ', 'ショ', 'ジャ', 'ジュ'}
KATAKANA |= {'ジョ', 'ニャ', 'ニュ', 'ニョ', 'ミャ', 'ミュ', 'ミョ', 'ヒャ', 'ヒュ', 'ヒョ', 'チャ'}
KATAKANA |= {'チュ', 'チョ', 'リャ', 'リュ', 'リョ', 'ヴァ', 'ヴィ', 'ヴェ', 'ー', 'ン'}


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
    message.send('皆でご飯を食べに行きたい人は「はい」と入力してください <!here>')
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
    for i_chunk in range(n_teams):
        yield attendee_list[i_chunk * len(attendee_list) // n_teams:(i_chunk + 1) * len(attendee_list) // n_teams]


@respond_to('終了')
def end(message):
    message.send('募集を終了します <!here>')
    g_status['is_open'] = False
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
    g_status['attendee_list'] = []
