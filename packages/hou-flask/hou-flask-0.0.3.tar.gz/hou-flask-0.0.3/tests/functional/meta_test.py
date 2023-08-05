"""
Unit tests intended to help test the meta endpoints of
the application: e.g. `/version` and `/status`
"""
import rapidjson

import oss_auth


class MetaFunctionalTest:
    url = "/v1/meta"

    def test_status(self, test_app):
        resp = test_app.get(f"{self.url}/status")
        assert resp.status_code == 200

    def test_version(self, test_app):
        resp = test_app.get(f"{self.url}/version")
        assert resp.status_code == 200
        data = rapidjson.loads(resp.body)
        assert data["version"] == oss_auth.__version__
