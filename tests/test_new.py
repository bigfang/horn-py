import os
import re
from pathlib import Path

import inflection
import pytest

from . import execli, lint


class TestNew:
    def test_new_with_default_options(self, tmp_path, capsys):
        execli(f'new {tmp_path}')
        lint(tmp_path)
        captured = capsys.readouterr()
        fset = {i.name for i in tmp_path.glob('*')}

        assert len(re.findall(r'^.+create.+$', captured.err, re.M)) == \
            len([i for i in tmp_path.glob('**/*')])
        assert fset == {'.gitignore', 'app', 'tests', 'log', 'instance', 'MANIFEST.in',
                        'logging.ini', 'README.md', 'pyproject.toml', 'setup.cfg', 'setup.py'}
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
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert fset == {'.gitignore', 'app', 'tests', 'log', 'instance', 'MANIFEST.in',
                        'logging.ini', 'README.md', 'pyproject.toml', 'setup.cfg', 'setup.py'}
        assert 'user.py' not in {i.name for i in tmp_path.glob('app/**/*.py')}

    @pytest.mark.parametrize('opts', ['--bare'])
    def test_with_dot_target_should_be_convert_to_proj(self, tmp_path, opts):
        cwd = os.getcwd()

        wdir = tmp_path / 'foo_bar'
        os.mkdir(str(wdir))
        os.chdir(str(wdir))
        execli(f'new . {opts}')
        os.chdir(cwd)

        lint(wdir)

        with open(wdir / 'README.md') as f:
            text = f.read()
            assert '# FooBar\n' in text
            assert '# .\n' not in text
            assert '\nProject .' not in text

    @pytest.mark.parametrize('opts', ['--app=foobar'])
    def test_new_with_options_app(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foobar' in fset
        assert 'FooBar' not in fset

    @pytest.mark.parametrize('opts', ['--proj=FooBar'])
    def test_new_with_options_proj(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' in fset
        assert 'foobar' not in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)

    @pytest.mark.parametrize('opts', ['--pypi https://pypi.doubanio.com/simple'])
    def test_new_with_options_pypi(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' in fset
        assert 'foobar' not in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'pyproject.toml') as f:
            text = f.read()
            assert re.search('^url = "https://pypi.doubanio.com/simple"$', text, re.M)

    @pytest.mark.parametrize('opts', ['--app=foobar --proj=FooBar --pypi=https://pypi.doubanio.com/simple'])
    def test_new_with_options_app_proj_pypi(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foobar' in fset
        assert 'FooBar' not in fset
        assert 'user.py' in {i.name for i in tmp_path.glob('foobar/**/*.py')}
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)
        with open(tmp_path / 'pyproject.toml') as f:
            text = f.read()
            assert re.search('^url = "https://pypi.doubanio.com/simple"$', text, re.M)

    @pytest.mark.parametrize('opts', ['--app=foo_bar', '--app=FooBar'])
    def test_new_app_should_be_underscore(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foo_bar' in fset
        assert 'FooBar' not in fset

    @pytest.mark.parametrize('opts', ['--proj=foo_bar', '--proj=FooBar'])
    def test_new_with_proj_should_be_camel(self, tmp_path, opts):
        execli(f'new {tmp_path} {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' in fset
        assert 'foo_bar' not in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)


class TestRepo:
    @pytest.mark.parametrize('opts', ['--json={"app":"foobar","bare":true}'])
    def test_from_local(self, tmp_path, opts):
        options = execli(f'new {tmp_path} ./horn/templates {opts}')
        lint(tmp_path)

        assert options['<from>'] == './horn/templates'
        with open(tmp_path / 'pyproject.toml') as f:
            text = f.read()
            assert re.search(r'^from = ".+/horn/templates"$', text, re.M)
            assert '\napp_name = "foobar"\n' in text
            assert '\nbare = true\n' in text

    @pytest.mark.xfail(reason='remote repo not ready')
    def test_remote_repo(self):
        assert False

    # @pytest.mark.parametrize('checkout', ['', 'master'])
    # def test_remote_with_wrong_repo(self, tmp_path, checkout, capsys):
    #     repo = 'https://gist.github.com/bb1f8b136f5a9e4abc0bfc07b832257e.git'
    #     with pytest.raises(SystemExit):
    #         execli(f'new {tmp_path} {repo} {checkout}')
    #     captured = capsys.readouterr()

    #     assert 'Error: Project template not found\n' == captured.out

    @pytest.mark.parametrize('opts', ['--json={"app":"foobar","proj":"FooBar"}'])
    def test_with_json_config(self, tmp_path, opts):
        opts = execli(f'new {tmp_path} ./horn/templates {opts}')
        lint(tmp_path)
        fset = {i.name for i in tmp_path.glob('*')}

        assert 'app' not in fset
        assert 'foobar' in fset
        assert 'FooBar' not in fset
        with open(tmp_path / 'README.md') as f:
            text = f.read()
            assert re.search('^# FooBar$', text, re.M)

    def test_with_file_config(self, tmp_path):
        file_opt = Path(__file__).parent.joinpath('fixture.json')
        options = execli(f'new {tmp_path} ./horn/templates --file={file_opt}')
        lint(tmp_path)

        assert options['<from>'] == './horn/templates'
        with open(tmp_path / 'pyproject.toml') as f:
            text = f.read()
            assert re.search(r'^from = ".+/horn/templates"$', text, re.M)
            assert '\napp_name = "ohmygod"\n' in text
            assert 'bare' not in text

    @pytest.mark.parametrize('opts', ['--json={"app":"foobar","bare":true}'])
    def test_json_config_should_override_file_config(self, tmp_path, opts):
        file_opt = Path(__file__).parent.joinpath('fixture.json')
        options = execli(f'new {tmp_path} ./horn/templates {opts} --file={file_opt}')
        lint(tmp_path)

        assert options['<from>'] == './horn/templates'
        with open(tmp_path / 'pyproject.toml') as f:
            text = f.read()
            assert re.search(r'^from = ".+/horn/templates"$', text, re.M)
            assert '\napp_name = "foobar"\n' in text
            assert '\nbare = true\n' in text
