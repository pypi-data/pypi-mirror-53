from uuid import uuid4

import pytest
from flask import Flask, g

from oss_auth.daos.permission_dao import Permission, Role
from oss_auth.exceptions import (
    MissingPermissionsException,
    ParameterNotPresentException,
)
from oss_auth.utils.authorization import require_org_permissions

from ...utils.factories import AccountFactory


class RequireAccountOrgPermissionsTest:
    @require_org_permissions(Permission.create_department)
    def _my_func(self, organization_id=None):
        return organization_id

    def test_when_no_organization_id__raises_exception(self):
        with pytest.raises(ParameterNotPresentException) as exc_info:
            self._my_func()

        assert "{}._my_func".format(self.__module__) in str(exc_info.value)

    def test_when_account_missing_override_permissions_and_not_same_org__raises_exception(
        self
    ):
        account = AccountFactory()
        with Flask("blah").app_context():
            g._current_account = account.id
            with pytest.raises(MissingPermissionsException):
                self._my_func(organization_id=uuid4())

    def test_when_account_has_override_permissions__no_exception(self):
        account = AccountFactory(role_name=Role.superuser.value)
        with Flask("blah").test_request_context():
            g._current_account = account.id
            org_id = uuid4()
            resp = self._my_func(organization_id=org_id)
            assert resp == org_id
