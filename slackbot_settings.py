import os

# botアカウントのトークンを指定
API_TOKEN = os.environ.get('slack_token')

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = '何言ってるんでしょうね、こいつ'

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']

# デプロイ権限をもつ管理ユーザ名のリスト
# export paccho_admin_users=hoge,foo,bar のようにカンマ区切りで複数指定できる
ADMIN_USER_NAME_LIST = os.environ.get('paccho_admin_users', '').split(',')

# char_scores.tsv の絶対パスを設定
THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CHAR_SCORES_FILE_PATH = os.path.join(THIS_FILE_PATH, 'data/char_scores.tsv')
