from copier import copy


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'app': opts.get('--app') or 'app',
        'proj': opts.get('<folder>').split('/')[-1].capitalize(),
        'bare': opts.get('--bare') or False,
        'pypi': opts.get('--pypi') or 'pypi.org',
        'repo': opts.get('--repo')
    }

    bindings.update(opts)

    copy('./templates/horn_proj', bindings.get('folder'), data=bindings)
