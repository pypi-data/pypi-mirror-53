from uuid import uuid4

import pytest

from oss_auth.daos.account_dao import AccountDAO
from oss_auth.database import DB
from oss_auth.exceptions import NotLoggedInException
from oss_auth.services.authentication_service import (
    CognitoService,
    get_account_by_token,
    logout_account,
)
from tests.utils.conditionals import (
    skip_unless_cognito_tests_enabled,
    skip_unless_create_cognito_tests_enabled,
)
from tests.utils.factories.base_factory import random_email, random_string

from ...utils.factories.account import AccountFactory, TokenFactory


class LogoutAccountTest:
    def test_when_token_not_exists__no_error(self):
        logout_account("fake")

    def test_when_token_exists__deletes_token(self):
        token = TokenFactory()
        logout_account(token.token)
        resp = DB.execute_query(
            "SELECT COUNT(*) FROM oss_auth.token WHERE token = %s", (token.token,)
        )
        assert resp[0][0] == 0


class GetAccountByTokenTest:
    def test_when_no_token__raises_not_logged_in_exception(self):
        with pytest.raises(NotLoggedInException):
            get_account_by_token("fake")

    def test_when_token__returns_user_id(self):
        token = TokenFactory()
        resp = get_account_by_token(token.token)
        assert resp == token.account_id


class LoginUserTest:
    @skip_unless_cognito_tests_enabled
    def test_when_valid__returns_token(self):
        token = CognitoService.login_user("test@timmartin.me", "P@ssw0rd")
        assert _get_token(token).token == token


class RegisterUserTest:
    @skip_unless_create_cognito_tests_enabled
    def test_when_valid__creates_user(self):
        username = random_email()
        account = CognitoService.register_user(username, "P@ssw0rd")
        resp = AccountDAO.get_account_info(account["id"])
        assert resp.username == username


class GetOrCreateAccountTest:
    def test_when_existing__returns_existing_account(self):
        account = AccountFactory()
        account_info, created = CognitoService._get_or_create_account(
            account.cognito_id, account.email
        )
        assert created is False
        assert account_info["id"] == account.id

    def test_when_does_not_exist__creates_and_returns_account(self):
        cognito_id = uuid4()
        account_info, created = CognitoService._get_or_create_account(
            cognito_id, f"{random_string()}@{random_string()}"
        )
        assert created is True
        assert account_info["cognito_id"] == cognito_id


class CreateTokenTest:
    def test_when_expiration_is_none__sets_expiration_to_default_and_returns_token(
        self
    ):
        account = AccountFactory()
        resp = CognitoService._create_token(
            account.id, random_string(), random_string()
        )
        assert _get_token(resp)


def _get_token(token):
    return DB.execute_query(
        "SELECT * FROM token WHERE token.token = %s", (token,), expect_one=True
    )
