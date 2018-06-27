"""fabric for lambda func."""
from fabric.api import local, lcd, settings

CFN = 'aws cloudformation'
S3_BUCKET = 'test-sam-cli'


def build(func_name):
    """依存ファイルDL."""
    with lcd('./'):
        local('pwd')
        local(f'pip install -r requirements.txt -t {func_name}/build')
        local(f'cp {func_name}/*.py {func_name}/build/')


def package(template_path):
    """Lambdaパッケージ化S3upload."""
    with settings(warn_only=True):
        # エラーでも警告のみので後続の処理が続く
        local(f'aws s3 mb s3://{S3_BUCKET}')
    with lcd(f'{template_path}'):
        cmd = 'sam package '\
              f'--template-file template.yaml '\
              '--output-template-file packaged.yaml '\
              f'--s3-bucket {S3_BUCKET}'
        local(cmd)


def deploy(stack_name):
    """Lambdaデプロイ."""
    with lcd(f'./'):
        cmd = 'sam deploy '\
            '--template-file packaged.yaml '\
            f'--stack-name {stack_name} '\
            '--capabilities CAPABILITY_IAM'
        local(cmd)