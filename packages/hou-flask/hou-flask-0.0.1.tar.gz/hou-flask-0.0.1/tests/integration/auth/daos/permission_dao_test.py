from oss_auth.daos.permission_dao import PermissionDAO, Role
from tests.utils.factories import (
    AccountFactory,
    DepartmentFactory,
    OrganizationAccountFactory,
)
from tests.utils.factories.department import DepartmentAccountFactory


class GetRolePermissionsTest:
    def test_when_no_role__returns_empty_set(self):
        resp = PermissionDAO.get_role_permissions(Role.no_role.value)
        assert resp == frozenset()


class GetAccountRolesForDepartmentTest:
    def test_when_not_in_org__returns_default_role_only(self):
        account = AccountFactory()
        dep = DepartmentFactory()
        resp = PermissionDAO.get_account_roles_for_department(account.id, dep.id)
        assert resp == {account.role_name}

    def test_when_in_org__returns_default_and_org_role(self):
        org_account = OrganizationAccountFactory()
        dep = DepartmentFactory(organization=org_account.organization)
        resp = PermissionDAO.get_account_roles_for_department(
            org_account.account_id, dep.id
        )
        assert resp == {org_account.account.role_name, org_account.role_name}

    def test_when_in_department__returns_department_org_and_default_roles(self):
        dep_account = DepartmentAccountFactory()
        resp = PermissionDAO.get_account_roles_for_department(
            dep_account.account_id, dep_account.department_id
        )
        assert resp == {
            dep_account.role_name,
            dep_account.organization_account.role_name,
            dep_account.account.role_name,
        }

    def test_when_in_parent_department__returns_parent_department_role(self):
        dep_account = DepartmentAccountFactory()
        child = DepartmentFactory(
            parent=dep_account.department, organization=dep_account.organization
        )
        resp = PermissionDAO.get_account_roles_for_department(
            dep_account.account_id, child.id
        )
        assert resp == {
            dep_account.role_name,
            dep_account.organization_account.role_name,
            dep_account.account.role_name,
        }

    def test_when_not_in_parent_department__returns_child_department_only(self):
        dep = DepartmentFactory()
        child = DepartmentAccountFactory(
            department__parent=dep, organization=dep.organization
        )
        resp = PermissionDAO.get_account_roles_for_department(
            child.account_id, child.department_id
        )
        assert resp == {
            child.role_name,
            child.organization_account.role_name,
            child.account.role_name,
        }

    def test_when_in_child_and_parent__returns_child_department_and_parent_department(
        self
    ):
        parent = DepartmentAccountFactory()
        child = DepartmentAccountFactory(
            department__parent=parent.department,
            organization=parent.organization,
            organization_account=parent.organization_account,
            account=parent.account,
        )
        resp = PermissionDAO.get_account_roles_for_department(
            child.account_id, child.department_id
        )
        assert resp == {
            child.role_name,
            child.organization_account.role_name,
            child.account.role_name,
            parent.role_name,
        }
