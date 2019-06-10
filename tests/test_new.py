import re

import inflection
import pytest

from . import execli


class TestNew:
    def test_new_with_default_options(self, tmp_path, capsys):
        execli(f'new {tmp_path}')
        captured = capsys.readouterr()
        fset = {i.name for i in tmp_path.glob('*')}

        assert len(re.findall(r'^.+create.+$', captured.out, re.M)) == \
            len([i for i in tmp_path.glob('**/*') if not i.is_dir()])
        assert fset == {'logging.ini', 'app', 'pytest.ini', 'test', 'README.md',
                        'Pipfile', '.gitignore', 'instance', 'log', 'project.toml'}
        assert 'user.py' in {i.name for i in tmp_path.glob('app/models/*py')}
        assert 'user.py' in {i.name for i in tmp_path.glob('app/schemas/*.py')}
        assert 'user.py' in {i.name for i in tmp_path.glob('app/views/*.py')}
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            directory = inflection.camelize(tmp_path.name)
            assert re.search(f'^# {directory}$', text, re.M)

    @pytest.mark.parametrize('opts', ['--bare'])
    def test_new_bare_project(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert fset == {'logging.ini', 'app', 'pytest.ini', 'test', 'README.md',
                        'Pipfile', '.gitignore', 'instance', 'log', 'project.toml'}
        assert 'user.py' not in {i.name for i in tmp_path.glob('app/**/*.py')}

    @pytest.mark.parametrize('opts', ['--app=foobar'])
    def test_new_with_options_app(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foobar' in fset
        assert 'FooBar' not in fset

    @pytest.mark.parametrize('opts', ['--proj=FooBar'])
    def test_new_with_options_proj(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' in fset
        assert 'foobar' not in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)

    @pytest.mark.parametrize('opts', ['--pypi doubanio.com'])
    def test_new_with_options_pypi(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' in fset
        assert 'foobar' not in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'Pipfile') as f:
            text = f.read()
            assert re.search('^url = "https://doubanio.com/simple"$', text, re.M)

    @pytest.mark.parametrize('opts', ['--app=foobar --proj=FooBar --pypi=doubanio.com'])
    def test_new_with_options_app_proj_pypi(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foobar' in fset
        assert 'FooBar' not in fset
        assert 'user.py' in {i.name for i in tmp_path.glob('foobar/**/*.py')}
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)
        with open(tmp_path / 'Pipfile') as f:
            text = f.read()
            assert re.search('^url = "https://doubanio.com/simple"$', text, re.M)

    @pytest.mark.parametrize('opts', ['--app=foo_bar', '--app=FooBar'])
    def test_new_app_should_be_underscore(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foo_bar' in fset
        assert 'FooBar' not in fset

    @pytest.mark.parametrize('opts', ['--proj=foo_bar', '--proj=FooBar'])
    def test_new_with_proj_should_be_camel(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' in fset
        assert 'foo_bar' not in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)


class TestRepo:
    def test_repo_without_config(self, tmp_path):
        options = execli(f'new {tmp_path} ./horn/templates')

        assert options['<from>'] == './horn/templates'
        with open(tmp_path / 'project.toml') as f:
            text = f.read()
            assert re.search(r'^from = ".+/horn/templates"$', text, re.M)

    @pytest.mark.skip(reason='remote repo not ready')
    @pytest.mark.parametrize('opts', ['--json='])
    def test_repo_remote(self, tmp_path, opts):
        repo = 'https://github.com/bigfang/horn-py-tpl.git'
        options = execli(f'new {tmp_path} {repo}')

        assert options['<from>'] == repo
        with open(tmp_path / 'project.toml') as f:
            assert re.search(r'^from = "{repo}"$', f.read(), re.M)

    @pytest.mark.xfail(reason='remote repo not ready')
    @pytest.mark.parametrize('opts', ['--json={"app": "foobar"}'])
    def test_repo_with_json_config(self, tmp_path, opts):
        opts = execli(f'new {tmp_path} ./horn/templates {opts}')
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foobar' in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)

    @pytest.mark.xfail(reason='remote repo not ready')
    def test_repo_with_file_config(self):
        assert False

    @pytest.mark.xfail(reason='remote repo not ready')
    def test_repo_json_config_should_override_file_config(self):
        assert False
