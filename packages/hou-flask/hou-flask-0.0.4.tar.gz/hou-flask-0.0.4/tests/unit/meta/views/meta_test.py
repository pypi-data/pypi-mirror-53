from unittest import mock

from oss_auth.views.meta import _check_database


class CheckDatabaseTest:
    @mock.patch("oss_auth.views.meta.DB")
    def test_when_exception__returns_error(self, database):
        database.cursor.side_effect = Exception
        resp = _check_database()
        assert not resp["available"]
