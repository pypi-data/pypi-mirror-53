from uuid import uuid4

import pytest
from werkzeug.routing import ValidationError

from oss_auth.utils.http import UUIDConverter


class UUIDConverterTest:
    def test_when_invalid__raises_validation_exception(self):
        converter = UUIDConverter(None)
        with pytest.raises(ValidationError):
            converter.to_python("invalid")

    def test_when_invalid_and_not_strict__raises_validation_exception(self):
        converter = UUIDConverter(None, strict=False)
        with pytest.raises(ValidationError):
            converter.to_python("invalid")

    def test_when_valid__returns_uuid(self):
        converter = UUIDConverter(None)
        expected = uuid4()
        resp = converter.to_python(str(expected))
        assert resp == expected

    def test_to_url__returns_str(self):
        converter = UUIDConverter(None)
        original = uuid4()
        resp = converter.to_url(original)
        assert resp == str(original)


from oss_auth.connexion_ext import UUIDParameterValidator


class ValidateParameterTest:
    def test_when_nullable_and_null__returns_empty(self):
        resp = UUIDParameterValidator.validate_parameter(
            "string", "null", {"schema": {"nullable": True, "type": "string"}}
        )
        assert resp is None
