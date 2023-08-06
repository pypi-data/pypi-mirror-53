from typing import List
from uuid import UUID

from houflask.auth.daos.permission_dao import Role
from ..daos.organization_account_dao import (
    OrganizationAccountDAO,
    UpsertAccountOrganization,
)

from ..daos.organization_dao import Organization, OrganizationDAO


class OrganizationService:
    organization_dao: OrganizationDAO
    organization_account_dao: OrganizationAccountDAO

    def __init__(
        self,
        organization_dao: OrganizationDAO,
        organization_account_dao: OrganizationAccountDAO,
    ):
        self.organization_dao = organization_dao
        self.organization_account_dao = organization_account_dao

    def create(self, name: str, owner_id: UUID, active: bool = True) -> Organization:
        org = self.organization_dao.create(name, active)
        self.organization_account_dao.upsert_account_orgs(
            [UpsertAccountOrganization(org.id, owner_id, Role.superuser.value)]
        )
        return org

    def update(self, id_: UUID, name: str, active: bool) -> Organization:
        return self.organization_dao.update(id_, name, active)

    def get_all_orgs(
        self, page: int, page_size: int, name_filter: str = ""
    ) -> List[Organization]:
        return self.organization_dao.get_all_orgs(page, page_size, name_filter)

    def get_orgs_for_account(self, account_id: UUID):
        return self.organization_dao.get_orgs_for_account(account_id)

    def get_org(self, organization_id: UUID) -> Organization:
        return self.organization_dao.get_org(organization_id)

    def organization_name_available(self, name: str) -> bool:
        return not self.organization_dao.org_name_exists(name)
