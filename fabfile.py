"""fabfile for cloudformation."""
from fabric.api import local, lcd, settings, abort, shell_env, task
from fabric.contrib.console import confirm
from fab import lambda_func
from fab.cfn import *


CFN = 'aws cloudformation'
S3_BUCKET = 'test-sam-cli'


def check():
    """テスト用."""
    # 環境変数はwith内のみ有効
    with shell_env(HOGE='fuga'):
        local('env | grep HOGE')
    # local用のcd
    with lcd('test-sam'):
        local('pwd')
        local('pip install -r requirements.txt -t hello_world/build')
        local('cp hello_world/*.py hello_world/build/')


def test():
    """動作確認."""
    with settings(warn_only=True):
        result = local('rm test', capture=True)
        print(result.stderr)
    # エラー時に後続の処理を行うか尋ねる
    if result.failed and not confirm('TEST failed. Continue anyway?'):
        abort('Abort at user request.')
    local('rm -rf test')


@task()
def build(func_name):
    """依存ファイルDL."""
    lambda_func.build(func_name)


@task()
def package(template_path):
    """package."""
    lambda_func.package(template_path)


@task()
def deploy(stack_name):
    """deploy."""
    lambda_func.deploy(stack_name)
