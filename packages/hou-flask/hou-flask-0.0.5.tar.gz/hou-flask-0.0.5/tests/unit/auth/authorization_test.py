import pytest

from oss_auth.daos.permission_dao import Permission
from oss_auth.exceptions import MissingPermissionsException
from oss_auth.utils.authorization import _require_permissions


class RequirePermissionsTest:
    def test_when_all_permissions__no_exception(self):
        _require_permissions(
            {Permission.get_all_orgs}, {Permission.get_all_orgs, Permission.update_org}
        )

    def test_when_missing_permissions__raises_exception(self):
        with pytest.raises(MissingPermissionsException):
            _require_permissions(
                {Permission.get_all_orgs},
                {Permission.update_org, Permission.create_org},
            )
