from flask import url_for


class TestSwagger(object):

    def test_swagger(self, testapp):
        resp = testapp.get(url_for('flask-apispec.swagger-ui'))
        assert resp.status_code == 200
        assert 'swagger' in resp.body.decode()
