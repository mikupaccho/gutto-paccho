import os

# botアカウントのトークンを指定
API_TOKEN = os.environ.get('slack_token')

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = '何言ってるんでしょうね、こいつ'

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']

# デプロイ権限をもつ管理ユーザ名のリスト
ADMIN_USER_NAME_LIST = ['']
