"""動作確認."""
from awscli.customizations.cloudformation.yamlhelper import yaml_parse
import os


def combine_template(template_path):
    """jsonを読み込みくっつける."""
    with open(template_path, 'r+') as file:
        data = yaml_parse(file.read())
    # dict_data = data
    for i in data['Resources']:
        rootpath = template_path.split('/')[0]
        path = f'{rootpath}/_template-{i}.yaml'
        if os.path.exists(path):
            with open(path) as subfile:
                data2 = yaml_parse(subfile.read())
                data['Resources'][i].update(data2)
    print(str(data))
    return str(data)


combine_template('s3/template-main.yaml')
