"""fabric for cfn."""
from fabric.api import local, task
import secrets
import boto3

CFN = 'aws cloudformation'


# @task(alias='mk')
# def create_stack(stack_name, template_path, *args):
#     """stack_name,template_path:スタック作成."""
#     cmd = f'{CFN} create-stack '\
#           f'--stack-name {stack_name} '\
#           f'--template-body file://{template_path} '\
#           '--capabilities CAPABILITY_IAM '
#     cmd_wait = f'{CFN} wait stack-create-complete '\
#                f'--stack-name {stack_name}'
# #     local(cmd)
#     local(cmd_wait)
#     event_stack(stack_name)


@task(alias='mk')
def create_stack(stack_name, template_path, **kwargs):
    """stack_name,template_path,key=val:スタック作成."""
    cf_conn = boto3.client('cloudformation')

    template = open(template_path, 'r')
    params = []
    if len(kwargs):
        for key, value in kwargs.items():
            add = {
                'ParameterKey': key,
                'ParameterValue': value
            }
            params.append(add)

    cf_conn.create_stack(
        StackName=stack_name,
        TemplateBody=template.read(),
        Parameters=params,
        Capabilities=['CAPABILITY_IAM'])
    cmd_wait = f'{CFN} wait stack-create-complete '\
               f'--stack-name {stack_name}'
    local(cmd_wait)
    event_stack(stack_name)


@task(alias='mkch')
def create_change_set(stack_name, template_path, **kwargs):
    """stack_name,template_path,key=val:変更セットを作成."""
    suffix = secrets.token_hex(4)

    cf_conn = boto3.client('cloudformation')

    template = open(template_path, 'r')
    params = []
    if len(kwargs):
        for key, value in kwargs.items():
            add = {
                'ParameterKey': key,
                'ParameterValue': value
            }
            params.append(add)

    cf_conn.create_change_set(
        StackName=stack_name,
        TemplateBody=template.read(),
        Parameters=params,
        Capabilities=['CAPABILITY_IAM'],
        ChangeSetName=f'{stack_name}{suffix}')

    cmd_wait = f'{CFN} wait change-set-create-complete '\
               f'--change-set-name {stack_name}{suffix}'
    local(cmd_wait)


@task(alias='lsc')
def list_change_set(stack_name):
    """stack_name:変更セット一覧."""
    cmd = f'{CFN} list-change-sets '\
          f'--stack-name {stack_name} ' \
          f'--query "Summaries[]"'
    local(cmd)


@task(alias='cless')
def describe_change_set(stack_name, set_name):
    """stack_name,set_name:変更セット確認."""
    q = """
    {
        name: StackName,
        status: StackStatus
    }
    """

    cmd = f'{CFN} describe-change-set '\
        f'--stack-name {stack_name} '\
        f'--change-set-name {set_name} '\
        # '--output table '\
    # f'--query "Changes[].{q}"'
    local(cmd)


@task(alias='exe')
def exe_change_set(stack_name, set_name):
    """stack_name,set_name:変更セット実行."""
    cmd = f'{CFN} execute-change-set '\
        f'--stack-name {stack_name} '\
        f'--change-set-name {set_name}'
    local(cmd)


@task(alias='ck')
def check_template(template_path):
    """template_path:templateファイルをチェック."""
    cmd = f'cfn-lint --template {template_path}'
    local(cmd)


@task(alias='output')
def stack_output(stack_name):
    """stack_name:スタックのOutPut."""
    cmd = f'{CFN} describe-stacks '\
        f'--stack-name {stack_name} ' \
        '--query "Stacks[].Outputs[]"'
    local(cmd)


@task(alias='ls')
def list_stack():
    """スタック一覧."""
    q = """
    {
        name: StackName,
        status: StackStatus
    }
    """
    cmd = f'{CFN} describe-stacks --output table --query "Stacks[].{q}"'
    r = local(cmd, capture=True)
    print(r.stdout)


@task(alias='deta')
def detail_stack(stack_name):
    """stack_name:スタック詳細."""
    cmd = f'{CFN} describe-stacks '\
        f'--stack-name {stack_name}'
    local(cmd)


@task(alias='less')
def event_stack(stack_name):
    """stack_name:スタックイベント."""
    q = """
    {
        LogicalResourceId: LogicalResourceId,
        LogicalResourceId: LogicalResourceId,
        ResourceStatus: ResourceStatus,
        ResourceType: ResourceType,
        Reason: ResourceStatusReason
    }
    """
    cmd = f'{CFN} describe-stack-events '\
        f'--stack-name {stack_name} '\
        '--output table '\
        f'--query "StackEvents[].{q}"'
    local(cmd)


@task(alias='resou')
def stack_resources(stack_name):
    """スタックのリソース情報."""
    cmd = f'{CFN} list-stack-resources --stack-name {stack_name}'
    local(cmd)


@task(alias='del')
def del_stack(stack_name):
    """stack_name:スタック削除."""
    cmd = f'{CFN} delete-stack '\
          f'--stack-name {stack_name}'
    cmd_wait = f'{CFN} wait stack-delete-complete '\
               f'--stack-name {stack_name}'
    local(cmd)
    local(cmd_wait)


@task(alias='delc')
def del_change_set(stack_name, set_name):
    """stack_name,set_name:変更セット削除."""
    cmd = f'{CFN} delete-stack '\
          f'--stack-name {stack_name} '\
          f'--change-set-name {set_name}'
    cmd_list = f'{CFN} list-change-sets '\
               f'--stack-name {stack_name} ' \
               f'--query "Summaries[]"'
    local(cmd)
    local(cmd_list)
