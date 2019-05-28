import os
import toml


def get_proj_info():
    proj_file = 'project.toml'
    if not os.path.isfile(proj_file):
        print(f'Error: Can not found {proj_file}')
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


def validate_opts(opts):
    for k, v in opts.items():
        if k.startswith('<'):
            if ':' in v:
                print(f'Error: Options error, {k}: {v}')
                exit(1)
        if k == '<fields>':
            for attrs in v:
                if ':' not in attrs:
                    print(f'Error: Options error, {k}: {attrs}')
                    exit(1)


def validate_type(arg, types):
    if arg not in types:
        print(f'Error: Field type error, {arg}')
        exit(1)
    return types.get(arg)


def validate_attr(attrs, affixes, exclude=tuple()):
    diff = set(attrs) - set(exclude)
    for attr in diff:
        if attr not in affixes:
            print(f'Error: Unknown attribute, {attr}')
            exit(1)
    return dict(zip(diff, [True for i in diff]))
