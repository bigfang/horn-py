import pytest

from flask import url_for


class TestUser(object):

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, testapp, user):
        testapp.post_json(url_for('session.create'), {
            'username': user.username,
            'password': 'wordpass'
        })
        testapp.authorization = ('Bearer', user.token)

    def test_index(self, testapp, user):
        resp = testapp.get(url_for('user.index'))
        assert resp.status_code == 200

    def test_create(self, testapp):
        resp = testapp.post_json(url_for('user.create'), {
            'username': 'horn',
            'email': 'test@horn.example',
            'password': 'hornsecret'
        })
        assert resp.status_code == 201
        assert sorted(resp.json.keys()) == ['email', 'id', 'inserted_at',
                                            'token', 'updated_at', 'username']
        assert resp.json['username'] == 'horn'
        assert resp.json['email'] == 'test@horn.example'

    def test_show(self, testapp, user):
        resp = testapp.get(url_for('user.show', pk=user.id))
        assert resp.status_code == 200

    # TODO: implement it
    def test_update(self, testapp, user):
        # resp = testapp.put_json(url_for('user.update', pk=user.id), {})
        # assert resp.status_code == 200
        assert True

    def test_delete(self, testapp, user):
        resp = testapp.delete(url_for('user.delete', pk=user.id))
        assert resp.status_code == 200
