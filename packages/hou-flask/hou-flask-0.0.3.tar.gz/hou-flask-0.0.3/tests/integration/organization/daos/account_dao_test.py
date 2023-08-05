from uuid import uuid4

import pytest
from hou_flask_psycopg2 import SQLNotFoundException
from psycopg2 import DataError, IntegrityError

from oss_auth.daos.account_dao import (
    Account,
    AccountDAO,
    UpsertAccountOrganization,
    Username,
)
from oss_auth.utils.permission import Role
from tests.utils.factories import (
    AccountFactory,
    DepartmentAccountFactory,
    DepartmentFactory,
    OrganizationAccountFactory,
    OrganizationFactory,
)
from tests.utils.factories.base_factory import EmptyRelationship, random_string


class GetOrgsForAccountTest:
    def test_when_account_id_invalid__raises_data_error(self):
        with pytest.raises(DataError):
            AccountDAO.get_orgs_for_account("balh")

    def test_when_valid__returns_all_associations(self):
        account = AccountFactory()
        org_accounts = OrganizationAccountFactory.build_batch(3, account=account)

        resp = AccountDAO.get_orgs_for_account(account.id)

        expected_org_ids = {oa.organization_id for oa in org_accounts}
        actual_org_ids = {row.organization_id for row in resp}
        assert actual_org_ids == expected_org_ids


class UpsertAccountOrgsTest:
    def test_when_multiple_accounts_all_new__inserts_all_rows(self):
        org = OrganizationFactory()
        accounts = AccountFactory.build_batch(3)
        account_rows = [
            UpsertAccountOrganization(
                account_id=account.id,
                organization_id=org.id,
                role_name=Role.default.value,
            )
            for account in accounts
        ]
        resp = AccountDAO.upsert_account_orgs(account_rows)
        assert len(resp) == 3
        actual_accounts = AccountDAO.get_accounts_for_org(org.id)
        self._assert_upserted_accounts_equal_accounts(resp, actual_accounts)

    def test_when_multiple_accounts_all_existing__updates_all_rows(self):
        org = OrganizationFactory()
        accounts = AccountFactory.build_batch(3, role_name=Role.superuser.value)
        account_rows = [
            UpsertAccountOrganization(
                account_id=account.id,
                organization_id=org.id,
                role_name=Role.default.value,
            )
            for account in accounts
        ]
        OrganizationAccountFactory.build_distinct_batch(
            [{"account_id": u.account_id} for u in account_rows],
            organization=org,
            account=EmptyRelationship(),
        )
        resp = AccountDAO.upsert_account_orgs(account_rows)
        assert len(resp) == 3
        actual_accounts = AccountDAO.get_accounts_for_org(org.id)
        self._assert_upserted_accounts_equal_accounts(resp, actual_accounts)

    def test_when_multiple_accounts_some_new_some_existing__updates_and_inserts(self):
        org = OrganizationFactory()
        accounts = AccountFactory.build_batch(3, role_name=Role.superuser.value)
        account_rows = [
            UpsertAccountOrganization(
                account_id=account.id,
                organization_id=org.id,
                role_name=Role.default.value,
            )
            for account in accounts
        ]
        OrganizationAccountFactory.build_distinct_batch(
            [{"account_id": u.account_id} for u in account_rows[1:]],
            organization=org,
            account=EmptyRelationship(),
        )
        resp = AccountDAO.upsert_account_orgs(account_rows)
        assert len(resp) == 3
        actual_accounts = AccountDAO.get_accounts_for_org(org.id)
        self._assert_upserted_accounts_equal_accounts(resp, actual_accounts)

    def test_when_invalid_account_id__raises_sql_not_found_exception(self):
        org = OrganizationFactory()
        with pytest.raises(IntegrityError):
            AccountDAO.upsert_account_orgs(
                [UpsertAccountOrganization(org.id, uuid4(), Role.superuser.value)]
            )

    def test_when_invalid_org_id__raises_sql_not_found_exception(self):
        account = AccountFactory()
        with pytest.raises(IntegrityError):
            AccountDAO.upsert_account_orgs(
                [UpsertAccountOrganization(uuid4(), account.id, Role.superuser.value)]
            )

    def test_when_invalid_role_name__raises_integrity_error(self):
        org = OrganizationFactory()
        account = AccountFactory()
        with pytest.raises(IntegrityError):
            AccountDAO.upsert_account_orgs(
                [UpsertAccountOrganization(org.id, account.id, "notreal")]
            )

    @staticmethod
    def _assert_upserted_accounts_equal_accounts(upserted_accounts, accounts):
        accounts = [
            UpsertAccountOrganization(u.organization_id, u.account_id, u.role_name)
            for u in accounts
        ]
        assert sorted(upserted_accounts) == sorted(accounts)


class RemoveAccountOrgTest:
    def test_when_exists__deletes_org_account(self):
        org_account = OrganizationAccountFactory()
        AccountDAO.remove_account_org(
            org_account.organization_id, org_account.account_id
        )
        rows = AccountDAO.get_orgs_for_account(org_account.account_id)
        assert rows == []

    def test_when_not_exists__safely_returns(self):
        org = OrganizationFactory()
        account = AccountFactory()
        AccountDAO.remove_account_org(org.id, account.id)
        rows = AccountDAO.get_orgs_for_account(account.id)
        assert rows == []


class GetAccountOrgsTest:
    def test_when_missing_one__raises_sql_not_found_exception(self):
        org_account = OrganizationAccountFactory()
        with pytest.raises(SQLNotFoundException):
            AccountDAO.get_account_orgs(
                [
                    (org_account.organization_id, org_account.account_id),
                    (uuid4(), uuid4()),
                ]
            )

    def test_when_all_found__returns_account_rows(self):
        org_accounts = OrganizationAccountFactory.build_batch(2)
        resp = AccountDAO.get_account_orgs(
            [(ou.organization_id, ou.account_id) for ou in org_accounts]
        )
        assert len(resp) == 2
        assert {row.account_id for row in resp} == {
            ou.account_id for ou in org_accounts
        }

    def test_when_empty__returns_empty(self):
        resp = AccountDAO.get_account_orgs([])
        assert resp == []


class GetUsernameTest:
    def test_when_id_exists__returns_username(self):
        account = AccountFactory.build()
        username = AccountDAO.get_username(account.id)
        assert username.account_id == account.id
        assert username.username == account.email

    def test_when_id_not_exists__raises_not_found_exception(self):
        with pytest.raises(SQLNotFoundException):
            AccountDAO.get_username(uuid4())


class GetUserNamesTest:
    def test_when_name_filter_empty__returns_all_usernames_and_ids(self):
        accounts = AccountFactory.build_batch(3)
        expected_usernames = {Username(a.id, a.email) for a in accounts}
        resp = AccountDAO.get_usernames("", 0, 1000)
        assert expected_usernames.issubset(set(resp))

    @pytest.mark.parametrize(("name_filter",), [("%",), ("e%",), ("%t",), ("e%t",)])
    def test_when_percentage_sign_in_name_filter__finds_all_usernames_with_percentage_sign(
        self, name_filter
    ):
        AccountFactory.build_batch(2)
        target_account = AccountFactory(email="some%thing")
        expected_response = [Username(target_account.id, target_account.email)]

        resp = AccountDAO.get_usernames(name_filter, 0, 1000)
        assert expected_response == resp

    def test_when_name_exact_match__returns_username(self):
        account = AccountFactory()

        resp = AccountDAO.get_usernames(account.email, 0, 1000)
        assert [Username(account.id, account.email)] == resp

    def test_when_no_name_matches__returns_empty(self):
        AccountFactory.build_batch(3)
        name_filter = random_string()
        resp = AccountDAO.get_usernames(name_filter, 0, 1000)
        assert resp == []

    def test_when_multiple_pages__returns_distinct_case_insensitive_sorted_batches(
        self
    ):
        AccountFactory.build_batch(10)

        resp1 = AccountDAO.get_usernames("", 0, 5)
        resp2 = AccountDAO.get_usernames("", 1, 5)

        # ensure distinct batches
        assert set(resp1).isdisjoint(set(resp2))
        usernames1 = [u.username.lower() for u in resp1]
        usernames2 = [u.username.lower() for u in resp2]
        min_in_set2 = min(usernames2)
        max_in_set1 = max(usernames1)

        # Ensure every username in set 2 is greater
        # than every name in set 1 and vice versa
        assert all(max_in_set1 <= username for username in usernames2)
        assert all(min_in_set2 >= username for username in usernames1)


class GetUserNamesByOrgTest:
    def test_when_name_filter_empty__returns_all_usernames_and_ids_for_org(self):
        org = OrganizationFactory()
        org_accounts = OrganizationAccountFactory.build_batch(3, organization=org)

        expected_usernames = {
            Username(oa.account.id, oa.account.email) for oa in org_accounts
        }
        resp = AccountDAO.get_usernames_by_org("", org.id, 0, 1000)
        assert expected_usernames == set(resp)

    @pytest.mark.parametrize(("name_filter",), [("%",), ("e%",), ("%t",), ("e%t",)])
    def test_when_percentage_sign_in_name_filter__finds_all_usernames_with_percentage_sign(
        self, name_filter
    ):
        org = OrganizationFactory()
        OrganizationAccountFactory.build_batch(2, organization=org)
        target = OrganizationAccountFactory(
            organization=org, account__email="some%thing"
        )
        resp = AccountDAO.get_usernames_by_org(name_filter, org.id, 0, 1000)

        expected_response = [Username(target.account_id, target.account.email)]
        assert expected_response == resp

    def test_when_no_name_matches__returns_empty(self):
        org = OrganizationFactory()
        OrganizationAccountFactory.build_batch(2, organization=org)
        name_filter = random_string()

        resp = AccountDAO.get_usernames_by_org(name_filter, org.id, 0, 10)
        assert resp == []

    def test_when_some_matches_in_different_org__only_returns_name_with_org(self):
        org_accounts = OrganizationAccountFactory.build_batch(3)
        org = OrganizationFactory()

        resp = AccountDAO.get_usernames_by_org(
            org_accounts[0].account.email, org.id, 0, 1000
        )
        assert resp == []

    def test_when_second_page__skips_first_results(self):
        org = OrganizationFactory()
        OrganizationAccountFactory.build_batch(10, organization=org)

        resp1 = AccountDAO.get_usernames_by_org("", org.id, 0, 5)
        resp2 = AccountDAO.get_usernames_by_org("", org.id, 1, 5)

        # ensure distinct batches
        assert set(resp1).isdisjoint(set(resp2))
        usernames1 = [u.username.lower() for u in resp1]
        usernames2 = [u.username.lower() for u in resp2]
        min_in_set2 = min(usernames2)
        max_in_set1 = max(usernames1)

        # Ensure every username in set 2 is greater
        # than every name in set 1 and vice versa
        assert all(max_in_set1 <= username for username in usernames2)
        assert all(min_in_set2 >= username for username in usernames1)


class GetAccountInfoTest:
    def test_when_valid__returns_account(self):
        account = AccountFactory()

        resp = AccountDAO.get_account_info(account.id)

        assert resp == Account(username=account.email, id=account.id)

    def test_when_not_found__raises_sqlobject_not_found(self):
        with pytest.raises(SQLNotFoundException):
            AccountDAO.get_account_info(uuid4())
