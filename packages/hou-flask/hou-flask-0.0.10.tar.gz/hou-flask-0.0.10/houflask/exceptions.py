from uuid import UUID
from typing import AbstractSet

from hou_flask_psycopg2 import SQLNotFoundException
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden


class InvalidUsernamePasswordException(Unauthorized):
    pass


class NotLoggedInException(Unauthorized):
    pass


class ParameterNotPresentException(Exception):
    def __init__(self, function_name: str, parameter_name, *args):
        super().__init__(
            f'The "{parameter_name}" parameter was not present in the call to "{function_name}',
            *args,
        )


class OrganizationNotFound(NotFound, SQLNotFoundException):
    def __init__(self, id_: UUID, *args, **kwargs) -> None:
        super().__init__(f'Organization with id "{id_}" not found', *args, **kwargs)


class OrganizationNameUnavailable(BadRequest, SQLNotFoundException):
    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(f'Organization with name "{name}" not found', *args, **kwargs)


class DuplicateFeatureFlagException(BadRequest):
    def __init__(self, name):
        super().__init__(f"A feature flag with the name {name} already exists")


class MissingPermissionsException(Forbidden):
    def __init__(self, missing_permissions: AbstractSet[str], *args, **kwargs) -> None:
        missing = ", ".join(missing_permissions)
        super().__init__(
            f"The following permissions are missing: {missing}", *args, **kwargs
        )
