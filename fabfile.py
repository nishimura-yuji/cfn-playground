from fabric.api import local, task, run, cd, lcd, settings, abort, shell_env
from fabric.contrib.console import confirm
from fab import cfn, lambda_func


CFN = 'aws cloudformation'
S3_BUCKET = 'test-sam-cli'


def check2():
    with shell_env(HOGE='fuga'):
        local('echo $HOGE')
    local('echo $HOGE')

def check():
    """テスト用"""
    # 環境変数はwith内のみ有効
    with shell_env(HOGE='fuga'):
        local('env | grep HOGE')
    # local用のcd
    with lcd('test-sam'):
        local('pwd')
        local('pip install -r requirements.txt -t hello_world/build')
        local('cp hello_world/*.py hello_world/build/')


def test():
    with settings(warn_only=True):
        result = local('rm test', capture=True)
        print(result.stderr)
    # エラー時に後続の処理を行うか尋ねる
    if result.failed and not confirm("TEST failed. Continue anyway?"):
        abort("Abort at user request.")
    local('rm -rf test')


def flat_folder():
    with lcd('test-sam'):
        local('pwd')
        local('pip install -r requirements.txt -t hello_world/build')
        local('cp hello_world/*.py hello_world/build/')


def package(stack_name):
    with settings(warn_only=True):
        # エラーでも警告のみので後続の処理が続く
        local(f'aws s3 mb s3://{S3_BUCKET}')
    with lcd(f'{stack_name}'):
        cmd = 'sam package '\
            f'--template-file template.yaml '\
            '--output-template-file packaged.yaml '\
            f'--s3-bucket {S3_BUCKET}'
        local(cmd)


def deploy(stack_name):
    with lcd(f'{stack_name}'):
        cmd = 'sam deploy '\
            '--template-file packaged.yaml '\
            f'--stack-name {stack_name} '\
            '--capabilities CAPABILITY_IAM'
        local(cmd)


def show_stack(stack_name):
    cmd = f'{CFN} describe-stacks '\
        f'--stack-name {stack_name} ' \
        f'--query "Stacks[].Outputs"'
    local(cmd)


def list_stack():
    """スタック一覧"""
    cmd = f'{CFN} describe-stacks | grep -E  "StackName|StackStatus"'
    r = local(cmd,capture=True)
    print(r.stdout)


def detail_stack(stack_name):
    """スタック詳細"""
    cmd = f'{CFN} describe-stacks '\
        f'--stack-name {stack_name}'
    local(cmd)

def show_stack_resources(stack_name):
    cmd = f'{CFN} list-stack-resources --stack-name {stack_name}'
    local(cmd)

def del_stack(stack_name):
    """スタック削除"""
    cmd = f'{CFN} delete-stack '\
          f'--stack-name {stack_name}'
    cmd_wait = f'{CFN} wait stack-delete-complete '\
               f'--stack-name {stack_name}'
    local(cmd)
    local(cmd_wait)



def update_stack():
    cmd = ''
    local(cmd)
