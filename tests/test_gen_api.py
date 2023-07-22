import re

import pytest

from io import StringIO

from . import execli, lint


class TestGenAPI:
    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string:uniq:nonull:index content:text:default:awesome author:ref:users:nonull')])
    def test_gen_schema(self, proj_path, module, table, fields, capsys, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen api {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        mm = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re. M)
        ms = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re. M)
        mv = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/views/post.py)$', captured.err, re. M)
        for m in [mm, ms, mv]:
            assert m.group(1)
            genf = (proj_path / m.group(1))
            assert genf.is_file()
            assert lint(genf)

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string content:text author:ref:users')])
    def test_with_wrong_path(self, tmp_path, module, table, fields, capsys, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        with pytest.raises(SystemExit):
            execli(f'gen api {module} {table} {fields}', tmp_path)
        captured = capsys.readouterr()

        assert 'Error: Can not found pyproject.toml\n' == captured.out

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string content:json')])
    def test_should_convert_json_to_dict(self, proj_path, module, table, fields, capsys, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen api {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        mm = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re. M)
        ms = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re. M)
        assert mm.group(1)
        assert ms.group(1)

        with open(proj_path / mm.group(1)) as f:
            text = f.read()
            assert "\n    content = Column(db.JSON, doc='Post content')\n" in text

        with open(proj_path / ms.group(1)) as f:
            text = f.read()
            assert '\n    content = fields.Dict()\n' in text

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string author:ref:users')])
    def test_should_convert_ref_to_nest(self, proj_path, module, table, fields, capsys, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen api {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        mm = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re. M)
        ms = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re. M)
        assert mm.group(1)
        assert ms.group(1)

        with open(proj_path / mm.group(1)) as f:
            text = f.read()
            assert "\n    author = relationship('Author', back_populates='posts')\n" in text

        with open(proj_path / ms.group(1)) as f:
            text = f.read()
            assert "\n    author = fields.Nested('UserSchema')\n" in text

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string:nonull:dump content:text:uniq:load author:ref:users:default:1:exclude')])
    def test_should_ignore_useless_attrs(self, proj_path, module, table, fields, capsys, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen api {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        mm = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re. M)
        ms = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re. M)
        assert mm.group(1)
        assert ms.group(1)

        with open(proj_path / mm.group(1)) as f:
            text = f.read()
            assert re.search(r"^\s{4}title = .+nullable=False, .+$", text, re.M)
            assert re.search(r"^\s{4}content = .+unique=True, .+$", text, re.M)
            assert re.search(r"^\s{4}author_id = .+'users', default=1, .+$$", text, re.M)

        with open(proj_path / ms.group(1)) as f:
            text = f.read()
            assert "\n        dump_only = ('title', )\n" in text
            assert "\n        load_only = ('content', )\n" in text
            assert "\n        exclude = ('author', )\n" in text
