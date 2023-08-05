from functools import wraps
from typing import AbstractSet, Any, Callable, Dict, Set, Tuple, Optional
from uuid import UUID

from flask import g, request
from hou_flask_psycopg2 import Psycopg2Utils

from houflask.auth.daos.permission_dao import Permission, PermissionDAO
from houflask.exceptions import (
    MissingPermissionsException,
    NotLoggedInException,
    ParameterNotPresentException,
)
from houflask.auth.services.authentication_service import AuthenticationService

AUTH_COOKIE = "auth-token"
__all__ = ["AUTH_COOKIE", "AuthorizationService"]


class AuthorizationService:
    permission_dao: PermissionDAO
    authentication_service: AuthenticationService

    def __init__(self, db: Optional[Psycopg2Utils] = None):
        if db:
            self.init_db(db)

    def init_db(self, db: Psycopg2Utils):
        self.permission_dao = PermissionDAO(db)
        self.authentication_service = AuthenticationService(db)

    def require_global_permissions(
        self, *permissions: Permission
    ) -> Callable[[Callable], Callable]:
        required_permissions = frozenset(permissions)

        def _decorator(func: Callable) -> Callable:
            @wraps(func)
            def _wrapper(*args: Tuple[Any], **kwargs: Dict[Any, Any]) -> Any:
                account_id = self.get_current_account()
                account_role = self.permission_dao.get_account_role(account_id)
                user_permissions = self.permission_dao.get_role_permissions(
                    account_role
                )
                self._require_permissions(required_permissions, user_permissions)
                return func(*args, **kwargs)

            # pylint: disable=protected-access
            _wrapper._required_permissions = required_permissions  # type: ignore
            return _wrapper

        return _decorator

    def require_logged_in(self, func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            self.get_current_account()
            return func(*args, **kwargs)

        return _wrapper

    @staticmethod
    def _require_permissions(
        required_permissions: AbstractSet[Permission],
        actual_permissions: AbstractSet[str],
    ) -> None:
        missing_permissions = {
            p.value for p in required_permissions
        } - actual_permissions
        if missing_permissions:
            raise MissingPermissionsException(missing_permissions)

    def get_current_account(self) -> UUID:
        # pylint: disable=protected-access
        if not hasattr(g, "_current_account"):
            token = request.cookies.get(AUTH_COOKIE)
            if not token:
                raise NotLoggedInException
            g._current_account = self.authentication_service.get_account_by_token(token)
        return g._current_account

    def _verify_role_permissions(
        self,
        role_names: AbstractSet[str],
        required_permissions: AbstractSet[Permission],
    ) -> None:
        assert required_permissions, "Override permissions must be provided"
        all_permissions = set()  # type: Set[Permission]
        for role_name in role_names:
            all_permissions |= self.permission_dao.get_role_permissions(role_name)
        self._require_permissions(required_permissions, all_permissions)

    def _require_permissions_helper(
        self,
        *required_permissions: Permission,
        kwarg_name: str = None,
        get_roles_func: Callable = None,
    ):
        def _require_account_org_permissions_decorator(func: Callable) -> Callable:
            @wraps(func)
            def _require_account_org_permissions_wrapper(*args, **kwargs):
                if kwarg_name not in kwargs:
                    raise ParameterNotPresentException(
                        f"{func.__module__}.{func.__name__}", kwarg_name
                    )
                role_names = get_roles_func()(
                    self.get_current_account(), kwargs[kwarg_name]
                )
                self._verify_role_permissions(
                    set(role_names), set(required_permissions)
                )
                return func(*args, **kwargs)

            return _require_account_org_permissions_wrapper

        return _require_account_org_permissions_decorator

    def require_org_permissions(self, *required_permissions):
        return self._require_permissions_helper(
            *required_permissions,
            kwarg_name="organization_id",
            get_roles_func=lambda: self.permission_dao.get_account_roles_for_org,
        )
