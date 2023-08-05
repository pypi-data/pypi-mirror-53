import logging
import re
from datetime import date, datetime
from uuid import UUID

from connexion import App as ConnexionApp
from connexion.decorators.response import ResponseValidator
from connexion.decorators.validation import ParameterValidator, RequestBodyValidator
from connexion.json_schema import Draft4RequestValidator, Draft4ResponseValidator
from connexion.utils import TYPE_MAP, is_null, is_nullable
from flask import Flask
from jsonschema import draft4_format_checker, validators
from ultra_config import GlobalConfig
from werkzeug.routing import BaseConverter, ValidationError

__all__ = ["FlaskConnexionExtension"]
LOG = logging.getLogger(__name__)
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


class FlaskConnexionExtension:
    app: Flask = None
    connexion_app: ConnexionApp = None

    def init_app(self, connexion_app: ConnexionApp) -> Flask:
        self.connexion_app = connexion_app
        self.app = self.connexion_app.app
        self._init_url_converters()
        draft4_format_checker.checks(format="uuid")(self.verify_uuid)
        draft4_format_checker.checks(format="date-time")(self.verify_datetime)
        draft4_format_checker.checks(format="date")(self.verify_date)
        return self.app

    @GlobalConfig.inject(
        strict_validation="SCHEMA_VALIDATION_STRICT",
        validate_responses="SCHEMA_VALIDATION_VALIDATE_RESPONSES",
    )
    def add_api(
        self,
        swagger_file: str,
        strict_validation: bool = True,
        validate_responses: bool = False,
        **kwargs
    ):
        return self.connexion_app.add_api(
            swagger_file,
            validator_map=self.monkeypatch_jsonschema_validation(),
            strict_validation=strict_validation,
            validate_responses=validate_responses,
            **kwargs
        )

    @staticmethod
    def verify_uuid(value):
        return isinstance(value, UUID) or value is None

    @staticmethod
    def verify_datetime(value):
        return isinstance(value, datetime)

    @staticmethod
    def verify_date(value):
        return isinstance(value, date)

    @staticmethod
    def monkeypatch_jsonschema_validation():
        return {
            "body": _UUIDRequestBodyValidator,
            "parameter": _UUIDParameterValidator,
            "response": _UUIDResponseBodyValidator,
        }

    def _init_url_converters(self):
        self.app.url_map.converters["UUID"] = _UUIDConverter


def _custom_json_schema_extend(validator, _validators, version=None, types=None):
    all_validators = dict(validator.VALIDATORS)
    all_validators.update(_validators)
    all_types = dict(validator.DEFAULT_TYPES)
    types = types or {}
    all_types.update(types)
    return validators.create(
        meta_schema=validator.META_SCHEMA,
        validators=all_validators,
        version=version,
        default_types=all_types,
    )


class _UUIDConverter(BaseConverter):
    """
    UUID converter for the Werkzeug routing system.

    Shamelessly borrowed from https://github.com/wbolster/flask-uuid
    """

    def __init__(self, map_, strict=True):
        super(_UUIDConverter, self).__init__(map_)
        self.strict = strict

    def to_python(self, value):
        if self.strict and not UUID_RE.match(value):
            raise ValidationError()

        try:
            return UUID(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return str(value)


def _build_uuid_validator_class(validator):
    extra_types = {"string": (*validators.str_types, UUID, datetime, date)}
    TYPE_MAP.update({"string": lambda value: value})
    return _custom_json_schema_extend(validator, {}, types=extra_types)


class _UUIDRequestBodyValidator(RequestBodyValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            validator=_build_uuid_validator_class(Draft4RequestValidator),
            **kwargs
        )


class _UUIDResponseBodyValidator(ResponseValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            validator=_build_uuid_validator_class(Draft4ResponseValidator),
            **kwargs
        )


class _UUIDParameterValidator(ParameterValidator):
    # pylint: disable=inconsistent-return-statements
    @staticmethod
    def validate_parameter(parameter_type, value, param, param_name=None):
        if value is not None:
            if is_nullable(param) and is_null(value):
                return
            schema = param.get("schema", {})

            if schema.get("type") == "string" and schema.get("format") == "uuid":
                try:
                    UUID(value)
                except ValueError as exc:
                    return str(exc)
            else:
                return ParameterValidator.validate_parameter(
                    parameter_type, value, param, param_name
                )
        return None
