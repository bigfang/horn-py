import os
import toml


def get_proj_info():
    proj_file = 'project.toml'
    if not os.path.isfile(proj_file):
        print(f'Can not found {proj_file}.')
        exit(1)
    data = toml.load(proj_file)
    project = data['project']
    return {
        'target': project.get('directory'),
        'proj': project.get('project_name'),
        'app': project.get('app_name'),
        'from': project.get('from'),
        'checkout': project.get('checkout')
    }


def merge_fields(base, attach={}):
    base.update(attach)
    return base


def validate_type(arg, types):
    if arg not in types:
        print(f'field type error: {arg}')
        exit(1)
    return types.get(arg)


def validate_attr(affix, *args):
    for arg in args:
        if arg not in affix:
            print(f'field type error: {":".join(args)}')
            exit(1)
    return dict(zip(args, [True for i in args]))
