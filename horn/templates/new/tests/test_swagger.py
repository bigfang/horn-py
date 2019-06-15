from flask import url_for


class TestSwagger(object):

    def test_swagger(self, client):
        resp = client.get(url_for('flask-apispec.swagger-ui'))
        assert resp.status_code == 200
        assert 'swagger' in resp.data.decode()
