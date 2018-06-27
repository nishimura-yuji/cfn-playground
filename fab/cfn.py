"""fabric for cfn."""
from fabric.api import local, task


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
        f'--query "Stacks[].Outputs"'
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


@task(alias='stackres')
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
