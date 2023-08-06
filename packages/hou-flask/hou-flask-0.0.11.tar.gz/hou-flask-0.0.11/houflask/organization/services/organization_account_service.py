from typing import List
from uuid import UUID

from ..daos.organization_account_dao import (
    OrganizationAccountDAO,
    OrganizationAccount,
    OrganizationAccountId,
    UpsertAccountOrganization,
)


class OrganizationAccountService:
    organization_account_dao: OrganizationAccountDAO

    def __init__(self, organization_account_dao: OrganizationAccountDAO):
        self.organization_account_dao = organization_account_dao

    def get_accounts_for_org(
        self,
        organization_id: UUID,
        name_filter: str = "",
        page: int = 0,
        page_size: int = 100,
    ) -> List[OrganizationAccount]:
        return self.organization_account_dao.get_accounts_for_org(
            organization_id, name_filter, page, page_size
        )

    def get_orgs_for_account(self, account_id: UUID) -> List[OrganizationAccount]:
        return self.organization_account_dao.get_orgs_for_account(account_id)

    def upsert_account_orgs(
        self, accounts: List[UpsertAccountOrganization]
    ) -> List[OrganizationAccount]:
        created_accounts = self.organization_account_dao.upsert_account_orgs(accounts)
        org_account_ids = [
            OrganizationAccountId(
                organization_id=account.organization_id, account_id=account.account_id
            )
            for account in created_accounts
        ]
        return self.organization_account_dao.get_account_orgs(org_account_ids)

    def remove_account_org(self, org_id: UUID, account_id: UUID) -> None:
        self.organization_account_dao.remove_account_org(org_id, account_id)
