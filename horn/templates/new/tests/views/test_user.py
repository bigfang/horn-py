from flask import url_for


class TestUser(object):

    def test_index(self, client, user, headers):
        resp = client.get(url_for('user.index'), headers=headers)
        assert resp.status_code == 200

    def test_create(self, client):
        payload = {
            'username': 'horn',
            'email': 'test@horn.example',
            'password': 'hornsecret'
        }
        resp = client.post(url_for('user.create'), json=payload)
        assert resp.status_code == 201
        assert set(resp.json.keys()) == {'email', 'id', 'inserted_at',
                                         'token', 'updated_at', 'username'}
        assert resp.json['username'] == 'horn'
        assert resp.json['email'] == 'test@horn.example'

    def test_show(self, client, user, headers):
        resp = client.get(url_for('user.show', pk=user.id), headers=headers)
        assert resp.status_code == 200

    # TODO: implement it
    def test_update(self, client, user, headers):
        # resp = client.put(url_for('user.update', pk=user.id), {})
        # assert resp.status_code == 200
        assert True

    def test_delete(self, client, user, headers):
        resp = client.delete(url_for('user.delete', pk=user.id), headers=headers)
        assert resp.status_code == 200
