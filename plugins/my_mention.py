import math
import numpy as np
import random
import unicodedata

from slackbot.bot import listen_to, respond_to, settings

from .katakana import get_katakanas_and_weights
from .utils.git_client import get_hash, git_pull

g_status = {
    'is_open': False,
    'is_silent': False,
    'attendee_list': [],
    'bento_attendee_list': [],
    'member_limit': None,
}

DEFAULT_LIMIT_MEMBER_COUNT = 6
KATAKANAS, WEIGHTS = get_katakanas_and_weights(settings.CHAR_SCORES_FILE_PATH)

# YESと判断されるメッセージリスト
YES_MESSAGE_LIST = ['はい', '行きます', 'おなかすいた']
BENTO_MESSAGE_LIST = ['弁当', 'コンビニ']


@listen_to('.+')
@respond_to('.+')
def listen(message):
    send_user = _get_user_name(message)
    if send_user:
        message_text = message.body['text']
        if g_status['is_open']:
            print(send_user, message_text)
            if message_text in YES_MESSAGE_LIST:
                g_status['attendee_list'].append('<@{}>'.format(send_user))
                message.react('+1')
            if message_text in BENTO_MESSAGE_LIST:
                g_status['bento_attendee_list'].append('<@{}>'.format(send_user))
                message.react('+1')
                message.react('bento')
    else:
        message.send('誰？')


@respond_to('(.+)?募集\s*(?:(\d+)\s*人組[で！。]?)?')
def start(message, how_to, member_limit=None):
    if member_limit is None:
        g_status['member_limit'] = DEFAULT_LIMIT_MEMBER_COUNT
    else:
        limit = int(unicodedata.normalize('NFKC', member_limit))
        g_status['member_limit'] = limit

    start_message = 'はらぺこ軍団全員集合〜「{}」って応答するパッチョ'.format(' か、'.join(YES_MESSAGE_LIST))
    start_message += '\n オフィスでお弁当を食べたい人は「{}」って応答するパッチョ'.format(' か、'.join(BENTO_MESSAGE_LIST))
    if g_status['member_limit'] != DEFAULT_LIMIT_MEMBER_COUNT:
        start_message += '\n {:d}人組で分けるパッチョ〜'.format(g_status['member_limit'])
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
    g_status['bento_attendee_list'] = []


@respond_to('終了')
def end(message):
    if not g_status['is_open']:
        message.send('何？')
        return

    end_message = '募集終了だパッチョ '
    if g_status['is_silent']:
        end_message += '(こっそり)'
    else:
        end_message += '<!here>'

    print(g_status['attendee_list'])
    # attendee_list をランダムに並び替え, メンバー数上限に応じてチームを分割
    attendee_list = list(set(g_status['attendee_list']))
    random.shuffle(attendee_list)
    splitted_attendee_list = _split_attendee_list(attendee_list, g_status['member_limit'])

    # 各グループごとに名前をランダム生成してslackに通知
    for attendee_group in splitted_attendee_list:
        team_name = np.random.choice(KATAKANAS, 2, replace=False, p=WEIGHTS)
        message.send('*チーム{}{}パッチョ*'.format(team_name[0], team_name[1]))
        for name in attendee_group:
            message.send(name)

    # 弁当組
    bento_attendee_list = list(set(g_status['bento_attendee_list']))
    if bento_attendee_list:
        team_name = np.random.choice(KATAKANAS, 1, replace=False, p=WEIGHTS)
        message.send('*チーム弁{}パッチョ*'.format(team_name[0]))
        for name in bento_attendee_list:
            message.send(name)

    # 募集状態のリセット
    _reset_state()


@respond_to('デプロイ')
def deploy(message):
    request_user_name = _get_user_name(message)
    if request_user_name in settings.ADMIN_USER_NAME_LIST:
        message.send('デプロイするぱっちょ')
        git_pull()
    else:
        message.send('{} はデプロイするには権限が足りないぱっちょ'.format(request_user_name))


@respond_to('バージョン')
def deploy(message):
    current_hash = get_hash()
    message.send('現在のぱっちょのバージョンは[{}] だぱっちょ'.format(current_hash))


def _get_user_name(message):
    """
    :param message:
    :return: str or None
    """
    user = message.body.get('user')
    if not user:
        return None
    user_name = message.channel._client.users[user]['name']
    return user_name
