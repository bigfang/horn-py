import os
import toml


def get_proj_info():
    proj_file = 'pyproject.toml'
    if not os.path.isfile(proj_file):
        print(f'Error: Can not found {proj_file}')
        exit(1)
    data = toml.load(proj_file)
    project = data['horn']
    return {
        'target': project.get('directory'),
        'proj': project.get('project_name'),
        'app': project.get('app_name'),
        'bare': project.get('bare'),
        'from': project.get('from'),
        'checkout': project.get('checkout')
    }


def merge_fields(base, attach={}):
    """
    >>> merge_fields({'a': 1})
    {'a': 1}
    >>> merge_fields({'a': 1}, {'b': 2})
    {'a': 1, 'b': 2}
    """
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
        if k == '<module>':
            if v[0].islower() or v == v.lower() or v == v.upper() or "_" in v:
                print('Error: Module name must be upper camel case')
                exit(1)


def validate_type(arg, types):
    """
    >>> types = {'string': 'String'}
    >>> validate_type('string', types)
    'String'
    >>> try:
    ...     validate_type('bbb', types)
    ... except:
    ...     pass
    Error: Field type error, bbb
    """
    if arg not in types:
        print(f'Error: Field type error, {arg}')
        exit(1)
    return types.get(arg)


def validate_attr(attrs, affixes, exclude=tuple()):
    """
    >>> attrs = ['nonull', 'load']
    >>> affixes = ('uniq', 'nonull', 'index')
    >>> exclude = ('none', 'required', 'dump', 'load', 'exclude')
    >>> validate_attr(attrs, affixes, exclude)
    {'nonull': True}
    >>> attrs.append('bbb')
    >>> try:
    ...     validate_attr(attrs, affixes, exclude)
    ... except:
    ...     pass
    Error: Unknown attribute, bbb
    """
    diff = set(attrs) - set(exclude)
    for attr in diff:
        if attr not in affixes:
            print(f'Error: Unknown attribute, {attr}')
            exit(1)
    return dict(zip(diff, [True for i in diff]))
