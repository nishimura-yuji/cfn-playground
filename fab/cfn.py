"""fabric for cfn."""
from fabric.api import local, task
import secrets

CFN = 'aws cloudformation'


@task(alias='mk')
def create_stack(stack_name, template_path):
    """スタック作成."""
    cmd = f'{CFN} create-stack '\
          f'--stack-name {stack_name} '\
          f'--template-body file://{template_path} '\
          '--capabilities CAPABILITY_IAM'
    cmd_wait = f'{CFN} wait stack-create-complete '\
               f'--stack-name {stack_name}'
    local(cmd)
    local(cmd_wait)


@task(alias='mkch')
def create_change_set(stack_name, template_path):
    """変更セットを作成."""
    suffix = secrets.token_hex(4)
    cmd = f'{CFN} create-change-set '\
          f'--stack-name {stack_name} '\
          f'--template-body file://{template_path} '\
          f'--change-set-name {stack_name}{suffix} '\
          '--capabilities CAPABILITY_IAM'
    cmd_wait = f'{CFN} wait change-set-create-complete '\
               f'--change-set-name {stack_name}{suffix}'
    local(cmd)
    local(cmd_wait)


@task(alias='lsc')
def list_change_set(stack_name):
    """変更セット一覧."""
    cmd = f'{CFN} list-change-sets '\
          f'--stack-name {stack_name} ' \
          f'--query "Summaries[]"'
    local(cmd)


@task(alias='descch')
def describe_change_set(stack_name, set_name):
    """変更セット確認."""
    cmd = f'{CFN} describe-change-set '\
        f'--stack-name {stack_name} '\
        f'--change-set-name {set_name}'
    local(cmd)


@task(alias='exech')
def exe_change_set(stack_name, set_name):
    """変更セット実行."""
    cmd = f'{CFN} execute-change-set '\
        f'--stack-name {stack_name} '\
        f'--change-set-name {set_name}'
    local(cmd)


@task(alias='ck')
def check_template(template_path):
    """templateファイルをチェック."""
    cmd = f'cfn-lint --template {template_path}'
    local(cmd)


@task(alias='desc')
def describe_stack(stack_name):
    """スタックの概要."""
    cmd = f'{CFN} describe-stacks '\
        f'--stack-name {stack_name} ' \
        '--query "Stacks[].Outputs"'
    local(cmd)


@task(alias='ls')
def list_stack():
    """スタック一覧."""
    cmd = f'{CFN} describe-stacks | grep -E  "StackName|StackStatus"'
    r = local(cmd, capture=True)
    print(r.stdout)


@task(alias='deta')
def detail_stack(stack_name):
    """スタック詳細."""
    cmd = f'{CFN} describe-stacks '\
        f'--stack-name {stack_name}'
    local(cmd)


@task(alias='event')
def event_stack(stack_name):
    """スタックイベント."""
    q = """
    {
        AStackName: StackName,
        LogicalResourceId: LogicalResourceId,
        LogicalResourceId: LogicalResourceId,
        ResourceStatus: ResourceStatus,
        Timestamp: Timestamp,
        ResourceType: ResourceType
    }
    """
    cmd = f'{CFN} describe-stack-events '\
        f'--stack-name {stack_name} '\
        f'--query "StackEvents[].{q}" --output table'
    local(cmd)


@task(alias='resou')
def stack_resources(stack_name):
    """スタックのリソース情報."""
    cmd = f'{CFN} list-stack-resources --stack-name {stack_name}'
    local(cmd)


@task(alias='dels')
def del_stack(stack_name):
    """スタック削除."""
    cmd = f'{CFN} delete-stack '\
          f'--stack-name {stack_name}'
    cmd_wait = f'{CFN} wait stack-delete-complete '\
               f'--stack-name {stack_name}'
    local(cmd)
    local(cmd_wait)


@task(alias='delc')
def del_change_set(stack_name, set_name):
    """変更セット削除."""
    cmd = f'{CFN} delete-stack '\
          f'--stack-name {stack_name} '\
          f'--change-set-name {set_name}'
    cmd_list = f'{CFN} list-change-sets '\
               f'--stack-name {stack_name} ' \
               f'--query "Summaries[]"'
    local(cmd)
    local(cmd_list)
