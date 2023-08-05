from datetime import datetime
from uuid import UUID, uuid4

import pytest
from psycopg2 import IntegrityError

from hou_flask_psycopg2 import SQLNotFoundException
from oss_auth.daos.authentication_dao import (
    create_account,
    create_token,
    delete_token,
    get_account_for_token,
)
from oss_auth.database import DB
from tests.utils.factories.account import AccountFactory, RoleFactory, TokenFactory
from tests.utils.factories.base_factory import random_string


class CreateUserTest:
    def test_when_role_name_not_exists__raises_exception(self):
        with pytest.raises(SQLNotFoundException):
            create_account("not_real", random_string(), uuid4())

    def test_when_role_name_exists__returns_new_id(self):
        role = RoleFactory.build()
        account_id = create_account(role.name, random_string(), uuid4())
        assert isinstance(account_id, UUID)
        resp = DB.execute_query(
            "SELECT COUNT(id) FROM oss_auth.account WHERE id=%s",
            (account_id,),
            expect_one=True,
        )
        assert resp[0] == 1


class CreateTokenTest:
    def test_when_auth_not_exists__raises_exception(self):
        with pytest.raises(IntegrityError):
            create_token(uuid4(), random_string(), random_string(), datetime.now())

    def test_when_auth_exists__returns_token(self):
        account = AccountFactory()
        resp = create_token(
            account.id, random_string(), random_string(), datetime.now()
        )
        assert isinstance(resp, str)


class GetUserForTokenTest:
    def test_when_token_not_exists__raises_sql_not_found_exception(self):
        with pytest.raises(SQLNotFoundException):
            get_account_for_token("fake")

    def test_when_token_exists__returns_user_id(self):
        token = TokenFactory()
        resp = get_account_for_token(token.token)
        assert resp == token.account_id


class DeleteTokenTest:
    def test_when_no_token__no_error(self):
        delete_token("not-real")

    def test_when_token__deletes_token(self):
        token = TokenFactory()
        delete_token(token.token)
        resp = DB.execute_query(
            "SELECT COUNT(*) FROM oss_auth.token WHERE token.token = %s", (token.token,)
        )
        assert resp[0][0] == 0
