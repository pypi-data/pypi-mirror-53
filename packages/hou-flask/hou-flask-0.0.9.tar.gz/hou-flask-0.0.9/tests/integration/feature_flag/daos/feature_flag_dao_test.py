from uuid import uuid4

import pytest
from hou_flask_psycopg2 import CustomJSON
from psycopg2.errors import ForeignKeyViolation

from oss_auth.daos.feature_flag_dao import (
    FeatureFlagDAO,
    FeatureVariant,
    NewFeatureVariant,
)
from oss_auth.database import DB
from oss_auth.exceptions import DuplicateFeatureFlagException
from tests.utils.factories import OrganizationFactory
from tests.utils.factories.base_factory import random_string
from tests.utils.factories.feature_flag import (
    FeatureFlagFactory,
    FeatureVariantFactory,
    FeatureVariantOrganizationFactory,
)


class CreateFeatureFlagTest:
    def test_when_valid__returns_feature_flag(self):
        name = random_string()
        FeatureFlagDAO.create_feature_flag(name, False)
        resp = FeatureFlagDAO.get_feature_flags()
        assert name in [ff.name for ff in resp]

    def test_when_duplicate_feature_flag_name__raises_exception(self):
        name = random_string()
        FeatureFlagDAO.create_feature_flag(name, False)
        with pytest.raises(DuplicateFeatureFlagException):
            FeatureFlagDAO.create_feature_flag(name, True)


class CreateFeatureVariantsTest:
    def test_when_empty__returns_empty(self):
        resp = FeatureFlagDAO.create_feature_variants([])
        assert resp == []

    def test_when_valid__returns_feature_variants(self):
        feature_flag = FeatureFlagFactory()
        variants = [
            NewFeatureVariant(feature_flag.name, True),
            NewFeatureVariant(feature_flag.name, False),
        ]
        resp = FeatureFlagDAO.create_feature_variants(variants)
        assert len(resp) == 2
        query = "SELECT COUNT(*) FROM feature_variant WHERE flag_name = %s"
        insert_count = DB.execute_query(query, (feature_flag.name,), expect_one=True)[0]
        assert insert_count == 2


class CreateFeatureVariantOrganizationTest:
    def test_when_variant_not_exists__raises_exception(self):
        variant = FeatureVariant(flag_name="not-real", variant=True, id=uuid4())
        org = OrganizationFactory()
        with pytest.raises(ForeignKeyViolation):
            FeatureFlagDAO.create_feature_variant_organization(
                variant.flag_name, variant.id, [org.id]
            )

    def test_when_empty__returns_empty(self):
        variant = FeatureVariantFactory()
        resp = FeatureFlagDAO.create_feature_variant_organization(
            variant.flag_name, variant.id, []
        )
        assert resp == []

    def test_when_valid__creates_variants_for_org(self):
        variant = FeatureVariantFactory()
        org_ids = [org.id for org in OrganizationFactory.build_batch(2)]
        resp = FeatureFlagDAO.create_feature_variant_organization(
            variant.flag_name, variant.id, org_ids
        )
        assert len(resp) == 2


class DeleteFeatureVariantOrganizationTest:
    def test_when_exists__deletes_organization(self, db_helper):
        variant = FeatureVariantOrganizationFactory()
        FeatureFlagDAO.delete_feature_variant_organization(
            variant.organization_id, variant.flag_name
        )
        db_helper.assert_database_has(
            "feature_variant_organization",
            {
                "organization_id": variant.organization_id,
                "flag_name": variant.flag_name,
            },
            0,
        )

    def test_when_not_exists__no_error(self):
        FeatureFlagDAO.delete_feature_variant_organization(uuid4(), "not-real")


class DeleteFeatureVariantsTest:
    def test_when_empty__safely_returns(self):
        FeatureFlagDAO.delete_feature_variants([])

    def test_when_valid__deletes_all(self):
        variants = FeatureVariantFactory.build_batch(2)
        ids = [var.id for var in variants]
        FeatureFlagDAO.delete_feature_variants(ids)
        count = DB.execute_query(
            "SELECT COUNT(*) FROM feature_variant WHERE id IN %s",
            (tuple(ids),),
            expect_one=True,
        )[0]
        assert count == 0


class GetFeatureFlagsTest:
    def test_when_valid__returns_all_feature_flags(self):
        feature_flags = FeatureFlagFactory.build_batch(2)
        resp = FeatureFlagDAO.get_feature_flags()
        assert {ff.name for ff in feature_flags}.issubset({row.name for row in resp})


class GetOrgVariantTest:
    def test_when_no_org_variant__returns_default(self):
        feature_flag = FeatureFlagFactory()
        org = OrganizationFactory()
        resp = FeatureFlagDAO.get_org_variant(feature_flag.name, org.id)
        assert resp == feature_flag.default_value

    def test_when_org_variant__returns_org_variant(self):
        org_variant = FeatureVariantOrganizationFactory(
            feature_variant__variant=CustomJSON(123)
        )
        resp = FeatureFlagDAO.get_org_variant(
            org_variant.flag_name, org_variant.organization_id
        )
        assert resp == 123
