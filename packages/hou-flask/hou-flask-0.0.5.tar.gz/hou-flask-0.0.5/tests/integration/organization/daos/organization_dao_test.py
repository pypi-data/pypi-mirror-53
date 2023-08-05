from uuid import uuid4

import pytest
from psycopg2 import IntegrityError

from hou_flask_psycopg2 import SQLNotFoundException
from oss_auth.daos.organization_dao import Organization, OrganizationDAO
from oss_auth.database import DB
from oss_auth.exceptions import OrganizationNameUnavailable, OrganizationNotFound
from tests.utils.factories.organization import OrganizationFactory


class CreateTest:
    def test_when_org_name_exists__raises_exception(self):
        OrganizationDAO.create("blah", False)
        with pytest.raises(OrganizationNameUnavailable):
            OrganizationDAO.create("blah", True)

    def test_when_valid__returns_org(self):
        actual = OrganizationDAO.create("blah", True)
        assert actual is not None
        expected = Organization(id=actual.id, name="blah", active=True)
        assert actual == expected

    def test_when_name_null__raises_exception(self):
        with pytest.raises(IntegrityError):
            OrganizationDAO.create(None, True)


class UpdateTest:
    def test_when_org_not_exists__raises_exception(self):
        with pytest.raises(OrganizationNotFound):
            OrganizationDAO.update(uuid4(), "blag", True)

    def test_when_new_name_exists__raises_exception(self):
        existing = OrganizationFactory.build()
        org = OrganizationFactory.build()
        with pytest.raises(OrganizationNameUnavailable):
            OrganizationDAO.update(org.id, existing.name, True)

    def test_when_name_null__raises_integrity_error(self):
        org = OrganizationFactory.build()
        with pytest.raises(IntegrityError):
            OrganizationDAO.update(org.id, None, True)

    def test_when_valid__returns_updated_org(self):
        org = OrganizationFactory.build()
        resp = OrganizationDAO.update(org.id, "newname", False)
        assert resp.name == "newname"
        assert resp.active is False

        query = "SELECT 1 FROM oss_auth.organization WHERE name = 'newname' AND active IS FALSE"
        resp = DB.execute_query(query, {})
        assert len(resp) == 1


class GetAllOrgsTest:
    def test_when_no_filter__returns_all(self):
        orgs = OrganizationFactory.build_batch(3)
        resp = OrganizationDAO.get_all_orgs()
        expected_ids = {org.id for org in orgs}
        actual_ids = {org.id for org in resp}
        assert expected_ids.issubset(actual_ids)

    def test_when_filter__only_returns_matches(self):
        org1 = OrganizationFactory(name="forreal")
        OrganizationFactory(name="another")

        resp = OrganizationDAO.get_all_orgs(name_filter="orrea")
        assert len(resp) == 1
        assert resp[0].id == org1.id

    def test_when_page_and_page_size__returns_offset(self):
        org1 = OrganizationFactory(name="forreals")
        OrganizationFactory(name="another")
        resp = OrganizationDAO.get_all_orgs(page=1, page_size=1)
        assert len(resp) == 1
        assert resp[0].id == org1.id

    def test_when_valid__returns_sorted_case_insensitvie(self):
        OrganizationFactory(name="ForReals")
        OrganizationFactory(name="blah")
        OrganizationFactory(name="Another")

        resp = OrganizationDAO.get_all_orgs()
        for i in range(len(resp) - 1):
            assert resp[i].name.lower() < resp[i + 1].name.lower()


class GetOrgTest:
    def test_when_org_not_exists__raises_exception(self):
        with pytest.raises(SQLNotFoundException):
            OrganizationDAO.get_org(uuid4())

    def test_when_org_exists__returns_org(self):
        expected = OrganizationFactory.build()
        actual = OrganizationDAO.get_org(expected.id)
        assert actual.id == expected.id


class GetOrgsTest:
    def test_when_all_found__returns_orgs(self):
        orgs = OrganizationFactory.build_batch(2)
        org_ids = {org.id for org in orgs}

        resp = OrganizationDAO.get_orgs(org_ids)

        assert len(resp) == 2

    def test_when_some_not_found__raises_sql_not_found_exception(self):
        org = OrganizationFactory()
        org_ids = {org.id, uuid4()}

        with pytest.raises(SQLNotFoundException):
            OrganizationDAO.get_orgs(org_ids)
