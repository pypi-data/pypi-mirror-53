from uuid import uuid4

from psycopg2.extras import DictCursor

from oss_auth.database import DB
from oss_auth.utils.permission import Role
from tests.functional_tests.base import FunctionalBase
from tests.utils.factories.account import TokenFactory
from tests.utils.factories.base_factory import random_string
from tests.utils.factories.organization import OrganizationFactory


class OrganizationCreateTest(FunctionalBase):
    url = "/v1/organization/organization"

    def test_when_invalid_parameters__returns_422(self, test_app):
        orgs = [
            {"name": "valid", "active": "invalid"},
            {"name": "@invalid", "active": True},
            {"name": "valid"},
            {"active": "valid"},
        ]
        token = TokenFactory(account__role_name="superuser")
        DB._db.connection.commit()
        for org in orgs:
            self.assert_post(test_app, org, 400, token=token)

    def test_when_valid__returns_id_201(self, test_app):
        token = TokenFactory(account__role_name="superuser")
        org = {"name": "valid", "active": True}
        resp = self.assert_post(test_app, org, 201, token=token)
        created_org = DB.execute_query(
            "SELECT name, active FROM oss_auth.organization WHERE id = %(id)s",
            {"id": resp.json["id"]},
            factory=DictCursor,
        )[0]
        assert dict(created_org) == org


class OrganizationUpdateTest(FunctionalBase):
    url = "/v1/organization/organization/{}"

    def test_when_invalid_parameters__returns_422(self, test_app):
        org_model = OrganizationFactory()
        token = TokenFactory(account__role_name="superuser")
        DB._db.connection.commit()
        orgs = [
            {"name": "valid", "active": "invalid"},
            {"name": "@invalid", "active": True},
            {"name": "valid"},
            {"active": "valid"},
        ]
        for org in orgs:
            self.assert_put(test_app, org, 400, org_model.id, token=token)

    def test_when_no_org__returns_404(self, test_app):
        token = TokenFactory(account__role_name="superuser")
        fake_org_id = uuid4()
        self.assert_put(
            test_app,
            {"name": "valid", "active": True, "id": fake_org_id},
            404,
            fake_org_id,
            token=token,
        )

    def test_when_valid__returns_200(self, test_app):
        org = OrganizationFactory()
        token = TokenFactory(account__role_name="superuser")
        self.assert_put(
            test_app,
            {"name": "valid", "active": True, "id": org.id},
            200,
            org.id,
            token=token,
        )


class OrganizationGetAllTest(FunctionalBase):
    url = "/v1/organization/organization"

    def test_filter_orgs(self, test_app):
        name_part = random_string()
        OrganizationFactory(name=f"ab{name_part}")
        OrganizationFactory(name=f"b{name_part}e")
        OrganizationFactory(name="zxy")
        token = TokenFactory(account__role_name="superuser")
        query = f"name_filter={name_part}&page=0&page_size=3"
        resp = self.assert_get(test_app, {}, 200, token=token, query=query)
        assert len(resp.json) == 2


class OrganizationGetOrgTest(FunctionalBase):
    url = "/v1/organization/organization/{}"

    def test_when_existing__returns_org(self, test_app, superuser_org):
        resp = self.assert_get(
            test_app, {}, 200, superuser_org[1].organization_id, token=superuser_org[0]
        )
        assert resp.json["name"] == superuser_org[1].organization.name

    def test_when_not_exists__returns_404(self, test_app):
        token = TokenFactory(account__role_name=Role.superuser.value)
        self.assert_get(test_app, {}, 404, uuid4(), token=token)

    def test_when_exists_but_user_no_permission__returns_403(self, test_app):
        token = TokenFactory(account__role_name=Role.default.value)
        self.assert_get(test_app, {}, 403, uuid4(), token=token)

    def test_when_not_logged_in__returns_401(self, test_app):
        resp = self.assert_get(test_app, {}, 401, uuid4())
        assert "login_url" in resp.json

    def test_when_invalid_id_format__returns_400(self, test_app):
        token = TokenFactory(account__role_name=Role.default.value)
        self.assert_get(test_app, {}, 400, "blah", token=token)


class OrganizationNameAvailabilityTest(FunctionalBase):
    url = "/v1/organization/organization/name"

    def test_when_name_available__returns_success_200(self, test_app):
        query = "name=available"
        token = TokenFactory(account__role_name="superuser")
        resp = self.assert_get(test_app, {}, 200, token=token, query=query)
        assert resp.json["available"] is True

    def test_when_name_unavailable__returns_failure_200(self, test_app):
        OrganizationFactory(name="unavailable")
        token = TokenFactory(account__role_name="superuser")
        query = "name=unavailable"
        resp = self.assert_get(test_app, {}, 200, token=token, query=query)
        assert resp.json["available"] is False
