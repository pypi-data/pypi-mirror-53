from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Union
from uuid import UUID

from hou_flask_psycopg2 import CustomJSON, Psycopg2Utils
from psycopg2.errors import UniqueViolation

from ...exceptions import DuplicateFeatureFlagException

_GET_ORG_VARIANT_NAME = "get_org_variant"


@dataclass
class FeatureFlag:
    name: str
    default_value: Union[int, str, bool, List, Dict]


@dataclass
class NewFeatureVariant:
    flag_name: str
    variant: Union[str, int, bool, List, Dict]


@dataclass
class FeatureVariant(NewFeatureVariant):
    id: UUID


@dataclass
class FeatureVariantOrganization:
    organization_id: UUID
    variant_id: Optional[UUID]
    flag_name: str


class FeatureFlagDAO:
    db: Psycopg2Utils

    def __init__(self, db: Psycopg2Utils):
        self.db = db

    def create_feature_flag(self, name, default_value) -> FeatureFlag:
        query = """
        INSERT INTO feature_flag (name, default_value)
        VALUES (%s, %s)
        RETURNING name, default_value
        """
        try:
            return self.db.execute_query_conversion(
                query, (name, CustomJSON(default_value)), FeatureFlag, expect_one=True
            )
        except UniqueViolation:
            raise DuplicateFeatureFlagException(name)

    def create_feature_variants(
        self, variants: Iterable[NewFeatureVariant]
    ) -> List[FeatureVariant]:
        query = """
        INSERT INTO feature_variant(flag_name, variant)
        VALUES {template}
        RETURNING id, flag_name, variant
        """
        to_insert = [(var.flag_name, CustomJSON(var.variant)) for var in variants]
        return self.db.bulk_insert(to_insert, FeatureVariant, query)

    def create_feature_variant_organization(
        self, flag_name: str, variant_id: UUID, organization_ids: Iterable[UUID]
    ) -> List[FeatureVariantOrganization]:
        query = """
        INSERT INTO feature_variant_organization(flag_name, variant_id, organization_id)
        VALUES {template}
        RETURNING flag_name, variant_id, organization_id
        """
        to_insert = [(flag_name, variant_id, org_id) for org_id in organization_ids]
        return self.db.bulk_insert(to_insert, FeatureVariantOrganization, query)

    def delete_feature_variant_organization(
        self, organization_id: UUID, flag_name: str
    ):
        query = """
        DELETE FROM feature_variant_organization
        WHERE organization_id = %s AND flag_name = %s
        """
        self.db.execute_query_without_fetch(query, (organization_id, flag_name))

    def delete_feature_variants(self, variant_ids: Iterable[UUID]):
        variant_ids = tuple(variant_ids)
        if not variant_ids:
            return
        query = "DELETE FROM feature_variant WHERE id IN %s"
        self.db.execute_query_without_fetch(query, (variant_ids,))

    def get_feature_flags(self) -> List[FeatureFlag]:
        query = """
        SELECT name, default_value
        FROM feature_flag
        """
        return self.db.execute_query_conversion(query, tuple(), FeatureFlag)

    def get_feature_variants(self) -> List[FeatureVariant]:
        query = """
        SELECT flag_name, variant, id
        FROM feature_variant
        """
        return self.db.execute_query_conversion(query, tuple(), FeatureVariant)

    def get_org_variant(self, name, organization_id):
        query = """
        SELECT COALESCE(fv.variant, ff.default_value)
        FROM feature_flag AS ff
        LEFT JOIN feature_variant_organization AS fvo 
          ON ff.name = fvo.flag_name AND organization_id = %s
        LEFT JOIN feature_variant AS fv ON ff.name = fv.flag_name
        WHERE ff.name = %s
        """
        return self.db.execute_query(query, (organization_id, name), expect_one=True)[0]
