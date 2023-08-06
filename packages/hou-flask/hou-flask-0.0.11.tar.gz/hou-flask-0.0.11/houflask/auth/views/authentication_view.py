import os
from typing import Dict

from flask import Response, request
from flask_wtf.csrf import generate_csrf
from hou_flask_psycopg2 import Psycopg2Utils
from ultra_config import GlobalConfig

from ..services.authentication_service import AuthenticationService
from ..services.authorization_service import AUTH_COOKIE
from ...connexion import FlaskConnexionExtension
from ...http import json_response

__all__ = ["AUTHENTICATION_VIEW"]


class _AuthenticationView:
    authentication_service: AuthenticationService

    def init_app(self, db: Psycopg2Utils, connexion_app: FlaskConnexionExtension):
        self.authentication_service = AuthenticationService(db)
        swagger_file = os.path.join(os.path.dirname(__file__), "..", "swagger-spec.yml")
        connexion_app.add_api(swagger_file, base_path="/v1/authentication")


AUTHENTICATION_VIEW = _AuthenticationView()


def register(body: Dict) -> Response:
    password = body["password"]
    confirm_password = body["confirm_password"]
    if not password == confirm_password:
        return json_response(
            {"message": "password and confirm password must match"}, 400
        )
    AUTHENTICATION_VIEW.authentication_service.register_user(
        body["email"], body["password"]
    )
    return json_response(
        {
            "message": (
                f"An email was sent to {body['email']} "
                f"Please click the link in the email to confirm your account"
            )
        },
        201,
    )


def login(body: Dict) -> Response:
    token = AUTHENTICATION_VIEW.authentication_service.login_user(
        body["username"], body["password"]
    )
    expires_in = 60 * 60 * 24 * 30 if body["remember"] else None
    return _set_token_cookie(token, json_response({"success": True}, 201), expires_in)


def logout() -> Response:
    token = request.cookies.get(AUTH_COOKIE)
    resp = json_response({"success": True, "login_url": "/login"})
    if token:
        AUTHENTICATION_VIEW.authentication_service.logout_account(token)
        _set_token_cookie("", resp, 0)
    return resp


def get_csrf_token():
    return json_response({"csrf_token": generate_csrf()})


def _set_token_cookie(
    token: str, response: Response, expires_in: int = None
) -> Response:
    secure = GlobalConfig.config["SECURE_COOKIES"]
    response.set_cookie(
        AUTH_COOKIE, token, path="/", max_age=expires_in, secure=secure, httponly=True
    )
    return response
