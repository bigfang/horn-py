import re

import pytest

from io import StringIO

from . import execli, lint


class TestGenModel:
    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string:uniq:nonull:index content:text:default:awesome author:ref:users:nonull')])
    def test_gen_model(self, proj_path, module, table, fields, capsys):
        execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+create.+\s+(\w+\/models/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert re.search(r'^class Post\(Model\):$', text, re.M)
            assert re.search(r"^\s{4}__tablename__ = 'posts'$", text, re.M)
            assert "\n    title = Column(db.String, unique=True, index=True, nullable=False, doc='Post title')\n" in text
            assert "\n    content = Column(db.Text, default='awesome', doc='Post content')\n" in text
            assert "\n    author_id = reference_col('users', nullable=False, doc='author id')" in text
            assert "\n    author = relationship('Author', back_populates='posts')" in text

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string content:text author:ref:users')])
    def test_with_wrong_path(self, tmp_path, module, table, fields, capsys):
        with pytest.raises(SystemExit):
            execli(f'gen model {module} {table} {fields}', tmp_path)
        captured = capsys.readouterr()

        assert 'Error: Can not found pyproject.toml\n' == captured.out

    @pytest.mark.parametrize('module,table,fields',
                             [('blogPost', 'posts', 'title:string content:text author:ref:users'),
                              ('Blog_Post', 'posts', 'title:string content:text author:ref:users'),
                              ('BLOGPOST', 'posts', 'title:string content:text author:ref:users'),
                              ('BLOG_POST', 'posts', 'title:string content:text author:ref:users'),
                              ('blog_post', 'posts', 'title:string content:text author:ref:users')])
    def test_module_name_should_be_camelcase(self, proj_path, module, table, fields, capsys):
        with pytest.raises(SystemExit):
            execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        assert 'Error: Module name must be upper camel case\n' == captured.out

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'blog_posts', 'title:string content:text author:ref:users'),
                              ('Post', 'BlogPosts', 'title:string content:text author:ref:users'),
                              ('Post', 'Blog_Posts', 'title:string content:text author:ref:users'),
                              ('Post', 'BLOG_POSTS', 'title:string content:text author:ref:users')])
    def test_table_name_should_be_lowercase(self, proj_path, module, table, fields, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('Y\n'))
        execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert re.search(r"^\s{4}__tablename__ = 'blog_posts'$", text, re.M)

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'xxx'),
                              ('Post', '', 'title:string content:text author:ref:users'),
                              ('', '', 'title:string content:text author:ref:users')])
    def test_with_wrong_opts(self, proj_path, module, table, fields, capsys):
        with pytest.raises(SystemExit):
            execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search('^Error: Options error, <.+>: .+$', captured.out, re.M)

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:int author:ref:users'),
                              ('Post', 'posts', 'title:string author:nest:users')])
    def test_with_wrong_field_type(self, proj_path, module, table, fields, capsys):
        with pytest.raises(SystemExit):
            execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search('^Error: Field type error, .+$', captured.out, re.M)

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string:null author:ref:users'),
                              ('Post', 'posts', 'title:string author:ref:users:xxx')])
    def test_with_wrong_attr(self, proj_path, module, table, fields, capsys, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda x: 'y')
        with pytest.raises(SystemExit):
            execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        assert re.search('^Error: Unknown attribute, .+$', captured.out, re.M)

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string:dump content:text:load author:ref:users:exclude'),
                              ('Post', 'posts', 'title:string:dump:load content:text author:default:1:ref:users:load'),
                              ('Post', 'posts', 'title:string:nonull:dump content:text author:default:1:ref:users:nonull')])
    def test_model_should_ignore_schema_attrs(self, proj_path, module, table, fields, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert 'dump' not in text
            assert 'load' not in text
            assert 'exclude' not in text

    @pytest.mark.parametrize('module,table,fields',
                             [('Post', 'posts', 'title:string content:text author:ref:users:default:1'),
                              ('Post', 'posts', 'title:string content:text author:default:1:ref:users'),
                              ('Post', 'posts', 'title:string content:text author:default:1:ref:users:nonull')])
    def test_ref_with_default(self, proj_path, module, table, fields, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('y\n'))
        execli(f'gen model {module} {table} {fields}', proj_path)
        captured = capsys.readouterr()

        match = re.search(r'^.+(?:create|conflict|identical).+\s+(\w+\/models/post.py)$', captured.err, re.M)
        assert match.group(1)
        genf = (proj_path / match.group(1))
        assert genf.is_file()
        assert lint(genf)
        with open(genf, 'r') as f:
            text = f.read()
            assert re.search(r'^class Post\(Model\):$', text, re.M)
            assert re.search(r"^ {4}__tablename__ = 'posts'$", text, re.M)
            assert re.search(r"^ {4}author_id = reference_col\('users', default=1, (nullable=False, )?doc='author id'\)$", text, re.M)
            assert "\n    author = relationship('Author', back_populates='posts')" in text
