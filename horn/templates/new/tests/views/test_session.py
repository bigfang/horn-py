from flask import url_for


class TestSession(object):

    def test_success_create(self, client, user):
        payload = {
            'username': user.username,
            'password': 'wordpass'
        }
        resp = client.post(url_for('session.create'), json=payload)
        assert resp.status_code == 201
        assert set(resp.json.keys()) == {'email', 'id', 'inserted_at',
                                         'token', 'updated_at', 'username'}
        assert resp.json['username'] == user.username
        assert resp.json['email'] == user.email

    def test_failed_create(self, client):
        payload = {
            'username': 'horn',
            'password': 'xxxxx'
        }
        resp = client.post(url_for('session.create'), json=payload)
        assert resp.status_code == 404

    def test_delete(self, client, login_user):
        headers = {
            'Authorization': f'Bearer {login_user.token}'
        }
        resp = client.delete(url_for('session.delete'), headers=headers)
        assert resp.status_code == 200
