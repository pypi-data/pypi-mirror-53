from typing import List, Tuple, Union
from uuid import UUID

from ..daos.feature_flag_dao import (
    FeatureFlag,
    FeatureFlagDAO,
    FeatureVariant,
    FeatureVariantOrganization,
    NewFeatureVariant,
)


class FeatureFlagService:
    def __init__(self, feature_flag_dao: FeatureFlagDAO):
        self.dao = feature_flag_dao

    def get_feature_flags(self) -> Tuple[List[FeatureFlag], List[FeatureVariant]]:
        feature_flags = self.dao.get_feature_flags()
        feature_variants = self.dao.get_feature_variants()
        return feature_flags, feature_variants

    def create_feature_flag(self, flag_name: str, default_value) -> FeatureFlag:
        return self.dao.create_feature_flag(flag_name, default_value)

    def create_feature_variant(self, flag_name: str, variant) -> FeatureVariant:
        return self.dao.create_feature_variants(
            [NewFeatureVariant(flag_name=flag_name, variant=variant)]
        )[0]

    def delete_feature_variant(self, variant_id: UUID):
        self.dao.delete_feature_variants([variant_id])

    def update_organization_variant(
        self, organization_id: UUID, variant_id: Union[UUID, None], flag_name: str
    ) -> FeatureVariantOrganization:
        self.dao.delete_feature_variant_organization(organization_id, flag_name)
        if variant_id is not None:
            return self.dao.create_feature_variant_organization(
                flag_name, variant_id, [organization_id]
            )[0]
        return FeatureVariantOrganization(
            organization_id=organization_id, variant_id=variant_id, flag_name=flag_name
        )
