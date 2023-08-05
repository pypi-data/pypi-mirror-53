from collections import namedtuple
from dataclasses import dataclass
from typing import List
from uuid import UUID

from hou_flask_psycopg2 import Psycopg2Utils

from houflask.auth.daos.authentication_dao import Username

OrganizationAccountId = namedtuple(
    "OrganizationUserId", ["organization_id", "account_id"]
)


@dataclass
class Account:
    username: str
    id: UUID


@dataclass(order=True)
class OrganizationAccount:
    username: str
    organization_id: UUID
    account_id: UUID
    role_name: str


@dataclass(order=True)
class DepartmentAccount:
    username: str
    department_id: UUID
    account_id: UUID
    role_name: str


@dataclass(order=True)
class UpsertAccountOrganization:
    organization_id: UUID
    account_id: UUID
    role_name: str


class OrganizationAccountDAO:
    def __init__(self, db: Psycopg2Utils):
        self.db = db

    def get_accounts_for_org(
        self,
        organization_id: UUID,
        name_filter: str = "",
        page: int = 0,
        page_size: int = 100,
    ) -> List[OrganizationAccount]:
        query = """
        SELECT 
          account.email AS username, 
          organization_account.account_id, 
          organization_account.organization_id,
          organization_account.role_name
        FROM account
        INNER JOIN organization_account ON account.id = organization_account.account_id
        WHERE organization_id = %s
          AND account.email ILIKE %s ESCAPE '='
        ORDER BY LOWER(account.email)
        LIMIT %s
        OFFSET %s
        """
        name_filter = self.db.unsafe_escape_like_string(
            name_filter, escape_character="="
        )
        return self.db.execute_query_conversion(
            query,
            (organization_id, f"%{name_filter}%", page_size, page * page_size),
            OrganizationAccount,
        )

    def get_orgs_for_account(self, account_id: UUID) -> List[OrganizationAccount]:
        query = """
        SELECT 
          a.email AS username,
          oa.account_id,
          oa.organization_id,
          oa.role_name
        FROM account AS a 
        INNER JOIN organization_account AS oa ON a.id = oa.account_id 
        WHERE a.id = %s
        """
        return self.db.execute_query_conversion(
            query, (account_id,), OrganizationAccount
        )

    def upsert_account_orgs(
        self, accounts: List[UpsertAccountOrganization]
    ) -> List[UpsertAccountOrganization]:
        query = """
        INSERT INTO organization_account (organization_id, account_id, role_name)
        VALUES {template}
        ON CONFLICT (organization_id, account_id)
          DO UPDATE 
            SET role_name = EXCLUDED.role_name
        RETURNING organization_id, account_id, role_name
        """
        return self.db.bulk_update(accounts, query, ("organization_id", "account_id"))

    def remove_account_org(self, org_id: UUID, account_id: UUID):
        query = """
        DELETE FROM organization_account
        WHERE organization_id = %s AND account_id = %s
        """
        self.db.execute_query_without_fetch(query, (org_id, account_id))

    def get_account_orgs(
        self, account_orgs: List[OrganizationAccountId]
    ) -> List[OrganizationAccount]:
        query = """
        WITH queried_accounts(organization_id, account_id) AS (
          VALUES {template}
        )
        SELECT DISTINCT ON (account.id, organization_account.organization_id, organization_account.role_name)
          account.email AS username, 
          organization_account.account_id, 
          organization_account.organization_id,
          organization_account.role_name
        FROM organization_account
        -- filter the orgs with a join
        INNER JOIN queried_accounts
          ON queried_accounts.organization_id = organization_account.organization_id
          AND queried_accounts.account_id = organization_account.account_id
        INNER JOIN account ON account.id = organization_account.account_id
        """
        return self.db.bulk_query(account_orgs, OrganizationAccount, query)

    def get_usernames_by_org(
        self, name_filter: str, org_id: UUID, page: int, page_size: int
    ) -> List[Username]:
        query = """
        SELECT email AS username, id AS account_id
        FROM account
        INNER JOIN organization_account oa ON account.id = oa.account_id
        WHERE email ILIKE %s ESCAPE '='
          AND organization_id = %s
        ORDER BY LOWER(email)
        LIMIT %s
        OFFSET %s
        """
        name_filter = self.db.unsafe_escape_like_string(
            name_filter, escape_character="="
        )
        return self.db.execute_query_conversion(
            query, (f"%{name_filter}%", org_id, page_size, page_size * page), Username
        )
