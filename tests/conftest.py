import os
import shutil

import pytest

from . import execli, lint


@pytest.fixture(scope='module',
                params=['', '--bare', '--app=foobar --proj=FooBar'])
def proj_path(tmp_path_factory, request):
    basetmp = tmp_path_factory.getbasetemp()
    path = basetmp / 'test_site'
    fn = tmp_path_factory.mktemp(str(path))
    execli(f'new {basetmp.name}/{fn.name} {request.param}')
    lint(fn)
    yield fn

    os.chdir(str(basetmp / '..'))
    shutil.rmtree(str(fn))
