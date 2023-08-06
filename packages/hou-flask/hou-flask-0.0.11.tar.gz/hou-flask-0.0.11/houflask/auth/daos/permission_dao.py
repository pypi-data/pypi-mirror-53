from enum import Enum
from typing import FrozenSet, Set, Tuple
from uuid import UUID

from beaker.cache import cache_region
from hou_flask_psycopg2 import Psycopg2Utils

from ...cache import LOCAL_LONG_TERM


__all__ = ["Permission", "PermissionDAO", "Role"]


class Permission(Enum):
    create_org = "organization:create"
    update_org = "organization:update"
    update_org_members = "organization:update:members"
    get_all_orgs = "organization:retrieve-all"
    get_org = "organization:retrieve"

    # Feature Flags
    get_feature_flags = "feature-flag:retrieve"
    create_feature_flag = "feature-flag:create"
    delete_feature_flag = "feature-flag:delete"
    update_organization_feature_variant = "feature-flag:organization:set-variant"


class Role(Enum):
    superuser = "superuser"
    default = "default"
    no_role = None


class PermissionDAO:
    db: Psycopg2Utils

    def __init__(self, db: Psycopg2Utils):
        self.db = db

    def get_account_role(self, account_id: UUID) -> str:
        query = """
        SELECT role_name
        FROM account
        WHERE id = %s
        """
        role_name, = self.db.execute_query(query, (account_id,), expect_one=True)
        return role_name

    @cache_region(LOCAL_LONG_TERM, "get_role_permissions")
    def get_role_permissions(self, role: str) -> FrozenSet[str]:
        if role == Role.no_role.value:
            return frozenset()
        query = """
        SELECT role_permission.permission_name
        FROM role_permission
        WHERE role_permission.role_name = %s
        """
        rows = self.db.execute_query(query, (role,))
        return frozenset(row.permission_name for row in rows)

    def get_account_roles_for_org(
        self, account_id: UUID, org_id: UUID
    ) -> Tuple[str, str]:
        query = """
        SELECT 
          account.role_name AS account_role,
          oa.role_name AS org_role
        FROM account
        LEFT JOIN organization_account oa 
          ON account.id = oa.account_id
          AND organization_id = %s
        WHERE account.id = %s
        """
        row = self.db.execute_query(query, (org_id, account_id), expect_one=True)
        return row.account_role, row.org_role

    def get_account_roles_for_department(
        self, account_id: UUID, department_id: UUID
    ) -> Set[str]:
        query = """
        SELECT role_name
        FROM account
        WHERE id = %(account_id)s

        UNION ALL

        SELECT role_name
        FROM department
        INNER JOIN organization_account
          ON department.organization_id = organization_account.organization_id
        WHERE department.id = %(department_id)s
          AND organization_account.account_id = %(account_id)s

        UNION ALL

        SELECT role_name
        FROM department
        INNER JOIN department parent
          ON parent.parent_path @> department.parent_path
        INNER JOIN department_account da 
          ON parent.id = da.department_id
          AND %(account_id)s = da.account_id
        WHERE department.id = %(department_id)s
        """
        params = {"account_id": account_id, "department_id": department_id}
        return {row[0] for row in self.db.execute_query(query, params)}
