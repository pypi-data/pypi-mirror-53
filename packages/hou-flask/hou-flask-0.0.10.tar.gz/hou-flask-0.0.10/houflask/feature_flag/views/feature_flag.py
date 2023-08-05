import dataclasses
from enum import Enum
from typing import Dict
from uuid import UUID

from flask import Response
from hou_flask_psycopg2 import Psycopg2Utils

from houflask.auth import AuthorizationService
from houflask.connexion import FlaskConnexionExtension
from houflask.feature_flag.daos.feature_flag_dao import FeatureFlagDAO
from houflask.http import empty_response, json_response, uuid_converter
from ..services.feature_flag_service import FeatureFlagService
import os

__all__ = ["FEATURE_FLAG_VIEW", "FeatureFlagPermission"]
_AUTH = AuthorizationService()


class _FeatureFlagView:
    feature_flag_service: FeatureFlagService

    def init_app(self, db: Psycopg2Utils, connexion_app: FlaskConnexionExtension):
        self.feature_flag_service = FeatureFlagService(FeatureFlagDAO(db))
        _AUTH.init_db(db)
        swagger_file = os.path.join(os.path.dirname(__file__), "..", "swagger-spec.yml")
        connexion_app.add_api(swagger_file, base_path="/v1/flag")


FEATURE_FLAG_VIEW = _FeatureFlagView()


class FeatureFlagPermission(Enum):
    get_feature_flags = "feature-flag:retrieve"
    create_feature_flag = "feature-flag:create"
    delete_feature_flag = "feature-flag:delete"
    update_organization_feature_variant = "feature-flag:organization:set-variant"


@_AUTH.require_global_permissions(FeatureFlagPermission.get_feature_flags)
def get_feature_flags() -> Response:
    feature_flags, feature_variants = (
        FEATURE_FLAG_VIEW.feature_flag_service.get_feature_flags()
    )
    return json_response(
        {
            "feature_flags": (dataclasses.asdict(ff) for ff in feature_flags),
            "variants": (dataclasses.asdict(fv) for fv in feature_variants),
        }
    )


@_AUTH.require_global_permissions(FeatureFlagPermission.create_feature_flag)
def create_feature_flag(body: Dict) -> Response:
    feature_flag = FEATURE_FLAG_VIEW.feature_flag_service.create_feature_flag(
        body["name"], body["default_value"]
    )
    return json_response(dataclasses.asdict(feature_flag), 201)


@_AUTH.require_global_permissions(FeatureFlagPermission.create_feature_flag)
def create_variant(body: Dict) -> Response:
    variant = FEATURE_FLAG_VIEW.feature_flag_service.create_feature_variant(
        body["flag_name"], body["variant"]
    )
    return json_response(dataclasses.asdict(variant), 201)


@_AUTH.require_global_permissions(FeatureFlagPermission.delete_feature_flag)
def delete_variant(variant_id: UUID) -> Response:
    FEATURE_FLAG_VIEW.feature_flag_service.delete_feature_variant(variant_id)
    return empty_response()


@_AUTH.require_global_permissions(
    FeatureFlagPermission.update_organization_feature_variant
)
def set_organization_variant(organization_id: UUID, body: Dict) -> Response:
    feature_variant_organization = FEATURE_FLAG_VIEW.feature_flag_service.update_organization_variant(
        organization_id, body["variant_id"], body["flag_name"]
    )
    return json_response(dataclasses.asdict(feature_variant_organization))
