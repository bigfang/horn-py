import pytest

from flask import url_for

from ..factories import UserFactory


@pytest.fixture
def login_user(client):
    user = UserFactory(password='iamloggedin')
    user.save()

    payload = {
        'username': user.username,
        'password': 'iamloggedin'
    }
    client.post(url_for('session.create'), json=payload)
    return user


class TestSession(object):

    def test_success_create(self, client, user):
        payload = {
            'username': user.username,
            'password': 'wordpass'
        }
        resp = client.post(url_for('session.create'), json=payload)
        assert resp.status_code == 201
        assert sorted(resp.json.keys()) == ['email', 'id', 'inserted_at',
                                            'token', 'updated_at', 'username']
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
