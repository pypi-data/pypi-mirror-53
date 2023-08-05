from oss_auth.daos.account_dao import AccountDAO
from oss_auth.utils.permission import Role
from tests.functional_tests.base import FunctionalBase
from tests.utils.factories import (
    AccountFactory,
    DepartmentAccountFactory,
    DepartmentFactory,
    OrganizationAccountFactory,
    OrganizationFactory,
    TokenFactory,
)
from tests.utils.factories.base_factory import random_string


class GetOrganizationsForAccountTest(FunctionalBase):
    url = "/v1/organization/account-self/organization-accounts"

    def test_when_valid__returns_organization_accounts(self, test_app):
        token = TokenFactory()
        OrganizationAccountFactory.build_batch(3, account=token.account)

        resp = self.assert_get(test_app, {}, 200, token=token)

        assert len(resp.json) == 3


class GetOrganizationForOwnAccountTest(FunctionalBase):
    url = "/v1/organization/account-self/organizations"

    def test_when_valid__return_organizations(self, test_app):
        token = TokenFactory()
        OrganizationAccountFactory.build_batch(3, account=token.account)

        resp = self.assert_get(test_app, {}, 200, token=token)

        assert len(resp.json) == 3


class UpsertAccountOrgTest(FunctionalBase):
    url = "/v1/organization/organization/{}/members/{}"

    def test_when_valid__adds_member(self, test_app, superuser_token):
        org = OrganizationFactory()
        account = AccountFactory()
        self.assert_put(
            test_app,
            {
                "account_id": account.id,
                "organization_id": org.id,
                "username": account.email,
                "role_name": Role.default.value,
            },
            200,
            org.id,
            account.id,
            token=superuser_token,
        )


class RemoveAccountOrgTest(FunctionalBase):
    url = "/v1/organization/organization/{}/members/{}"

    def test_when_valid__remove_account_org(self, test_app, superuser_token):
        org_account = OrganizationAccountFactory()
        self.assert_delete(
            test_app,
            {},
            204,
            org_account.organization_id,
            org_account.account_id,
            token=superuser_token,
        )
        rows = AccountDAO.get_orgs_for_account(org_account.account_id)
        assert rows == []


class GetUsernamesTest(FunctionalBase):
    url = "/v1/username"

    def test_when_valid__gets_usernames(self, test_app, superuser_token):
        account = AccountFactory()

        resp = self.assert_get(
            test_app,
            {"name_filter": str(account.email)[1:], "page": 0, "page_size": 10},
            200,
            token=superuser_token,
        )

        assert resp.json == [{"username": account.email, "account_id": str(account.id)}]
