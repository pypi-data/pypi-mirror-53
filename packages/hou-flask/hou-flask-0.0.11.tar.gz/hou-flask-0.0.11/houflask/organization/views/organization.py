import dataclasses
from enum import Enum
from typing import Dict
from uuid import UUID

from flask import Response, request
from hou_flask_psycopg2 import Psycopg2Utils

from houflask.auth import AuthorizationService
from houflask.connexion import FlaskConnexionExtension
from houflask.http import (
    json_response,
    dataclass_json_response,
    empty_response,
    uuid_converter,
)
from houflask.organization.daos.organization_account_dao import (
    OrganizationAccountDAO,
    UpsertAccountOrganization,
)

from houflask.organization.daos.organization_dao import OrganizationDAO
from houflask.organization.services.organization_account_service import (
    OrganizationAccountService,
)
from ..services.organization_service import OrganizationService
import os


_AUTH = AuthorizationService()


class Permission(Enum):
    create_org = "organization:create"
    update_org = "organization:update"
    update_org_members = "organization:update:members"
    get_all_orgs = "organization:retrieve-all"
    get_org = "organization:retrieve"


class _OrganizationView:
    organization_service: OrganizationService
    organization_account_service: OrganizationAccountService

    def init_app(self, db: Psycopg2Utils, connexion_app: FlaskConnexionExtension):
        self.organization_service = OrganizationService(
            OrganizationDAO(db), OrganizationAccountDAO(db)
        )
        self.organization_account_service = OrganizationAccountService(
            OrganizationAccountDAO(db)
        )
        _AUTH.init_db(db)
        swagger_file = os.path.join(os.path.dirname(__file__), "..", "swagger-spec.yml")
        connexion_app.add_api(swagger_file, base_path="/v1/organization")


ORGANIZATION_VIEW = _OrganizationView()


@_AUTH.require_global_permissions(Permission.create_org)
def create():
    data = request.get_json()
    org = ORGANIZATION_VIEW.organization_service.create(
        data["name"], _AUTH.get_current_account(), data["active"]
    )
    return json_response(dataclasses.asdict(org), status=201)


@_AUTH.require_global_permissions(Permission.get_all_orgs)
def get_all(page, page_size, name_filter=""):
    orgs = ORGANIZATION_VIEW.organization_service.get_all_orgs(
        page, page_size, name_filter
    )
    models = [dataclasses.asdict(org) for org in orgs]
    return json_response(models, 200)


@_AUTH.require_org_permissions(Permission.get_org)
def get_org(organization_id: UUID) -> Response:
    org = ORGANIZATION_VIEW.organization_service.get_org(organization_id)
    return json_response(dataclasses.asdict(org), 200)


@_AUTH.require_global_permissions(Permission.update_org)
def update(organization_id, body):
    org = ORGANIZATION_VIEW.organization_service.update(
        organization_id, name=body["name"], active=body["active"]
    )
    return json_response(dataclasses.asdict(org))


@_AUTH.require_global_permissions(Permission.get_all_orgs)
def organization_name_available():
    available = ORGANIZATION_VIEW.organization_service.organization_name_available(
        request.args["name"]
    )
    return json_response({"available": available})


def get_accounts_for_org(
    organization_id: UUID, page: int, page_size: int, name_filter: str = ""
) -> Response:
    accounts = ORGANIZATION_VIEW.organization_account_service.get_accounts_for_org(
        organization_id, name_filter, page, page_size
    )
    return dataclass_json_response(accounts)


def get_organization_accounts_for_own_account() -> Response:
    account_id = _AUTH.get_current_account()
    return dataclass_json_response(
        ORGANIZATION_VIEW.organization_account_service.get_orgs_for_account(account_id)
    )


def get_organizations_for_own_account() -> Response:
    account_id = _AUTH.get_current_account()
    return dataclass_json_response(
        ORGANIZATION_VIEW.organization_service.get_orgs_for_account(account_id)
    )


@uuid_converter(("organization_id", "account_id"))
@_AUTH.require_org_permissions(Permission.update_org_members)
def upsert_account_org(organization_id: UUID, account_id: UUID, body: Dict) -> Response:
    upsert_row = UpsertAccountOrganization(
        organization_id, account_id, body["role_name"]
    )
    return dataclass_json_response(
        ORGANIZATION_VIEW.organization_account_service.upsert_account_orgs(
            [upsert_row]
        )[0]
    )


@_AUTH.require_org_permissions(Permission.update_org_members)
def remove_account_org(organization_id: UUID, account_id: UUID) -> Response:
    ORGANIZATION_VIEW.organization_account_service.remove_account_org(
        organization_id, account_id
    )
    return empty_response()
