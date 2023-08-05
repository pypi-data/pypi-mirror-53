import pytest

from oss_auth.database import DB
from oss_auth.exceptions import NotLoggedInException
from oss_auth.utils.authorization import get_current_account

from houflask.auth.services.authorization_service import AUTH_COOKIE
from oss_auth.views.authentication import AUTH_COOKIE

from ..utils.conditionals import (
    skip_unless_cognito_tests_enabled,
    skip_unless_create_cognito_tests_enabled,
)
from ..utils.factories.account import TokenFactory
from ..utils.factories.base_factory import random_email, random_string
from .base import FunctionalBase


class RegisterTest(FunctionalBase):
    url = "/v1/authentication/register"

    def test_when_password_mismatch__raises_400_error(self, test_app):
        email = random_email()
        password = "P@ssw0rd"
        self.assert_post(
            test_app,
            {"email": email, "password": password, "confirm_password": "blahblah"},
            400,
        )

    @skip_unless_create_cognito_tests_enabled
    def test_when_passwords_match__creates_user(self, test_app):
        email = f"{random_string()}@{random_string()}.com"
        password = "P@ssw0rd"
        self.assert_post(
            test_app,
            {"email": email, "password": password, "confirm_password": password},
            201,
        )
        DB.execute_query(
            "SELECT 1 FROM account WHERE email = %s", (email,), expect_one=True
        )


class LoginTest(FunctionalBase):
    url = "/v1/authentication/login"

    @skip_unless_cognito_tests_enabled
    def test_when_valid_login__sets_token(self, test_app):
        email = "test@timmartin.me"
        password = "P@ssw0rd"
        resp = self.assert_post(
            test_app, {"username": email, "password": password, "remember": True}, 201
        )
        assert resp.headers["Set-Cookie"].startswith(f"{AUTH_COOKIE}=")


class GetCurrentAccountTest:
    def test_when_no_token(self, test_app):
        with test_app.app.test_request_context():
            with pytest.raises(NotLoggedInException):
                get_current_account()

    def test_when_token_not_exists(self, test_app):
        with test_app.app.test_request_context(
            headers={"Cookie": "{}=blah".format(AUTH_COOKIE)}
        ):
            with pytest.raises(NotLoggedInException):
                get_current_account()

    def test_when_token_valid__returns_id(self, test_app):
        token = TokenFactory()
        cookie = "{}={}".format(AUTH_COOKIE, token.token)
        with test_app.app.test_request_context(headers={"Cookie": cookie}):
            account_id = get_current_account()
            assert account_id == token.account_id


class LogoutTest(FunctionalBase):
    url = "/v1/authentication/logout"

    def test_when_logged_in__returns_200_and_deletes_cookie(
        self, test_app, superuser_token
    ):
        resp = self.assert_get(test_app, {}, 200, token=superuser_token)

        rows = DB.execute_query(
            "SELECT TRUE FROM oss_auth.token WHERE token = %s", (superuser_token.token,)
        )
        assert rows == []
        assert "login_url" in resp.json
        assert "auth-token=;" in resp.headers["Set-Cookie"]

    def test_when_not_logged_in__returns_200(self, test_app, superuser_token):
        self.assert_get(test_app, {}, 200)


class GetCSRFTokenTest(FunctionalBase):
    url = "/v1/authentication/csrf_token"

    def test_when_valid__returns_token(self, test_app):
        resp = self.assert_get(test_app, {}, 200)
        assert "csrf_token" in resp.json
