from flask import url_for


def _register_user(testapp):
    return testapp.post_json(url_for('user.create'), {
        'username': 'horn',
        'email': 'test@horn.example',
        'password': 'hornsecret'
    })


class TestSession(object):

    def test_success_create(self, testapp):
        _register_user(testapp)
        resp = testapp.post_json(url_for('session.create'), {
            'username': 'horn',
            'password': 'hornsecret'
        })
        assert resp.status_code == 201
        assert sorted(resp.json.keys()) == ['email', 'id', 'inserted_at',
                                            'token', 'updated_at', 'username']
        assert resp.json['username'] == 'horn'
        assert resp.json['email'] == 'test@horn.example'

    def test_failed_create(self, testapp):
        resp = testapp.post_json(url_for('session.create'), {
            'username': 'horn',
            'password': 'xxxxx'
        }, status=404)
        assert resp.status_code == 404

    def test_delete(self, testapp, login_user):
        resp = testapp.delete(url_for('session.delete'))
        assert resp.status_code == 200
