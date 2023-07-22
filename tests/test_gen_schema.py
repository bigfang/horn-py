import re

import pytest

from io import StringIO

from . import execli, lint


class TestGenSchema:
    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:string content:string author:nest:user'),
                              ('Post', '', 'title:string content:string author:nest:user'),
                              ('Post', 'Post', '')])
    def test_gen_schema(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen schema {module} {fields} {model_opt}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re. M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()

            if fields:
                assert "\n    title = fields.String()\n" in text
                assert "\n    content = fields.String()\n" in text
                assert "\n    author = fields.Nested('UserSchema')\n" in text
                assert "\n        fields = ('id', 'title', 'content', 'author', )\n" in text
            else:
                assert not re.search(r'^\s+fields.+$', text, re.M)

            if model:
                assert re.search(r'^from \w+\.models import Post$', text, re.M)
                assert "\nclass PostSchema(ModelSchema, SchemaMixin):\n" in text
                assert "\n        model = Post\n" in text
            else:
                assert "\nclass PostSchema(Schema, SchemaMixin):\n" in text

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:string content:string author:nest:user'),
                              ('Post', '', 'title:string content:string author:nest:user'),
                              ('Post', 'Post', '')])
    def test_with_wrong_path(self, tmp_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        with pytest.raises(SystemExit):
            execli(f'gen schema {module} {model_opt} {fields}', tmp_path)
        captured = capsys.readouterr()

        assert 'Error: Can not found pyproject.toml\n' == captured.out

    @pytest.mark.parametrize('module,model,fields',
                             [('blogPost', 'Post', 'title:string content:string author:nest:user'),
                              ('Blog_Post', '', 'title:string content:string author:nest:user'),
                              ('blog_post', 'Post', 'title:string content:string author:nest:user'),
                              ('BLOG_POST', 'Post', 'title:string content:string author:nest:user'),
                              ('BLOGPOST', 'Post', '')])
    def test_module_name_should_be_camelcase(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        with pytest.raises(SystemExit):
            execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        assert 'Error: Module name must be upper camel case\n' == captured.out

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'blog_post', 'title:string content:string author:nest:user'),
                              ('Post', 'BlogPost', 'title:string content:string author:nest:user'),
                              ('Post', 'Blog_Post', 'title:string content:string author:nest:user')])
    def test_model_name_should_be_camelcase(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert re.search(r"^class PostSchema\(.+\):$", text, re.M)
            assert "\n        model = BlogPost\n" in text

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', '', 'xxx'),
                              ('', '', 'title:string content:string author:nest:user')])
    def test_with_wrong_opts(self, proj_path, module, model, fields, capsys):
        model_opt = f'--model={model}' if model else ''
        with pytest.raises(SystemExit):
            execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search('^Error: Options error, <.+>: .+$', captured.out, re.M)

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:int content:string author:nest:user'),
                              ('Post', '', 'title:string content:string author:ref:user')])
    def test_with_wrong_field_type(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        with pytest.raises(SystemExit):
            execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search('^Error: Field type error, .+$', captured.out, re.M)

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:string:null author:ref:user'),
                              ('Post', '', 'title:string author:nest:user:xxx')])
    def test_with_wrong_attr(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        with pytest.raises(SystemExit):
            execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search('^Error: Unknown attribute, .+$', captured.out, re.M)

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:string:nonull content:string:dump author:nest:user'),
                              ('Post', '', 'title:string:uniq content:string:index author:nest:user')])
    def test_schema_should_ignore_model_attrs(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert 'null' not in text
            assert 'uniq' not in text
            assert 'index' not in text

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:string:dump:load author:nest:user'),
                              ('Post', 'Post', 'title:string:load:dump author:nest:user'),
                              ('Post', 'Post', 'title:string:dump:exclude author:nest:user'),
                              ('Post', '', 'title:string:dump:exclude:load author:nest:user:exclude:load')])
    def test_schema_meta_key_should_be_mutex(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        with pytest.raises(SystemExit):
            execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search(r'Error: Field attributes error, \[.+\] conflict', captured.out, re.M)

    @pytest.mark.parametrize('module,model,fields',
                             [('Post', 'Post', 'title:string author:nest:blog_user'),
                              ('Post', '', 'title:string author:nest:blogUser'),
                              ('Post', '', 'title:string author:nest:BlogUser'),
                              ('Post', '', 'title:string author:nest:Blog_User')])
    def test_nested_field_should_be_convert_to_camelcase(self, proj_path, module, model, fields, capsys, monkeypatch):
        model_opt = f'--model={model}' if model else ''
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen schema {module} {model_opt} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/schemas/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert "\n    author = fields.Nested('BlogUserSchema')\n" in text
