import rapidjson
from flask_webtest import TestApp

from houflask.auth.services.authorization_service import AUTH_COOKIE


class FunctionalBase:
    @classmethod
    def assert_post(
        cls, test_app: TestApp, params, status_code, *url_params, token=None, query=None
    ):
        url = cls._request(test_app, *url_params, token=token, query=query)
        resp = test_app.post(
            url,
            rapidjson.dumps(params),
            content_type="application/json",
            expect_errors=True,
        )
        return cls._assert_resp(resp, status_code)

    @classmethod
    def assert_get(
        cls, test_app: TestApp, params, status_code, *url_params, token=None, query=None
    ):
        url = cls._request(test_app, *url_params, token=token, query=query)
        resp = test_app.get(url, params, expect_errors=True)
        return cls._assert_resp(resp, status_code)

    @classmethod
    def assert_put(
        cls, test_app: TestApp, params, status_code, *url_params, token=None, query=None
    ):
        url = cls._request(test_app, *url_params, token=token, query=query)
        resp = test_app.put(
            url,
            rapidjson.dumps(params),
            content_type="application/json",
            expect_errors=True,
        )
        return cls._assert_resp(resp, status_code)

    @classmethod
    def assert_delete(
        cls, test_app: TestApp, params, status_code, *url_params, token=None, query=None
    ):
        url = cls._request(test_app, *url_params, token=token, query=query)
        resp = test_app.delete(
            url,
            rapidjson.dumps(params),
            content_type="application/json",
            expect_errors=True,
        )
        return cls._assert_resp(resp, status_code)

    @classmethod
    def _request(cls, test_app: TestApp, *url_params, token=None, query: str = None):
        if token:
            test_app.set_cookie(AUTH_COOKIE, token.token)
        url = cls._build_url(*url_params, query=query)
        return url

    @classmethod
    def _assert_resp(cls, resp, expected_status_code):
        assert (
            resp.status_code == expected_status_code
        ), f"{resp.status_code} != {expected_status_code}. body: {resp.body}"
        return resp

    @classmethod
    def _build_url(cls, *url_params, query=None):
        url = cls.url.format(*url_params)
        return url if not query else f"{url}?{query}"
