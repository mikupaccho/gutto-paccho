import os
import subprocess

GIT_BUN = 'git'


def git_pull():
    """
    git pull して自分のリポジトリを更新する
    :return:
    """
    subprocess.call([
        GIT_BUN,
        'pull'
    ], cwd=os.getcwd())


def get_hash():
    """
    git rev-parse --short HEAD
    :return:
    """
    result = subprocess.run(
        ' '.join([
            GIT_BUN,
            'rev-parse',
            '--short HEAD'
        ]),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=os.getcwd()
    )
    return result.stdout.decode('utf-8').strip()
