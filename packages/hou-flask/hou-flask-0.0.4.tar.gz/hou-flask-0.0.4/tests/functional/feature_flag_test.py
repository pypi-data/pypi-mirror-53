from uuid import uuid4

import rapidjson

from tests.functional_tests.base import FunctionalBase
from tests.utils.factories.base_factory import random_string
from tests.utils.factories.feature_flag import FeatureFlagFactory, FeatureVariantFactory


class GetFeatureFlagsTest(FunctionalBase):
    url = "/v1/flag/feature_flag"

    def test_when_valid__returns_feature_flags_and_variants(
        self, test_app, superuser_token
    ):
        feature1 = FeatureFlagFactory()
        feature2 = FeatureVariantFactory()
        resp = self.assert_get(test_app, {}, 200, token=superuser_token)
        flags = {flag["name"] for flag in resp.json["feature_flags"]}
        assert feature1.name in flags
        assert feature2.flag_name in flags
        variants = {
            (variant["flag_name"], variant["variant"])
            for variant in resp.json["variants"]
        }
        assert (feature2.flag_name, feature2.variant) in variants


class CreateFeatureFlagTest(FunctionalBase):
    url = "/v1/flag/feature_flag"

    def test_when_valid__creates_feature_flag(
        self, test_app, superuser_token, db_helper
    ):
        name = random_string()
        body = {"name": name, "default_value": True}
        resp = self.assert_post(test_app, body, 201, token=superuser_token)
        assert resp.json == body
        db_helper.assert_database_has(
            "feature_flag", {"name": name, "default_value": rapidjson.dumps(True)}
        )

    def test_when_duplicate_name__returns_400(self, test_app, superuser_token):
        flag = FeatureFlagFactory()
        body = {"name": flag.name, "default_value": True}
        self.assert_post(test_app, body, 400, token=superuser_token)


class CreateVariantTest(FunctionalBase):
    url = "/v1/flag/feature_variant"

    def test_when_valid__creates_variant(self, test_app, superuser_token):
        flag = FeatureFlagFactory()
        body = {"flag_name": flag.name, "variant": True}
        resp = self.assert_post(test_app, body, 201, flag.name, token=superuser_token)
        assert body.items() <= resp.json.items()


class DeleteVariantTest(FunctionalBase):
    url = "/v1/flag/feature_variant/{}"

    def test_when_valid__deletes_variant(self, test_app, superuser_token, db_helper):
        variant = FeatureVariantFactory()
        self.assert_delete(test_app, {}, 204, variant.id, token=superuser_token)
        db_helper.assert_database_has("feature_variant", {"id": variant.id}, 0)

    def test_when_does_not_exists__returns_successful_response(
        self, test_app, superuser_token
    ):
        self.assert_delete(test_app, {}, 204, uuid4(), token=superuser_token)
