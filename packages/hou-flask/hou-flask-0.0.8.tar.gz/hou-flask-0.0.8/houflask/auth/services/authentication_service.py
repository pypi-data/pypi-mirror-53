import base64
import hashlib
import hmac
import logging
from datetime import datetime, timedelta
from typing import Dict, Tuple
from uuid import UUID

import boto3
import rapidjson
from beaker.cache import cache_region
from hou_flask_psycopg2 import SQLNotFoundException, Psycopg2Utils
from jose import jwt
from ultra_config import GlobalConfig

from ..daos.authentication_dao import AuthenticationDAO
from ..daos.permission_dao import Role
from ...exceptions import NotLoggedInException
from ...cache import LOCAL_LONG_TERM

LOG = logging.getLogger(__name__)

__all__ = ["AuthenticationService"]


class AuthenticationService:
    db: Psycopg2Utils
    authentication_dao: AuthenticationDAO

    def __init__(self, db: Psycopg2Utils):
        self.authentication_dao = AuthenticationDAO(db)

    @GlobalConfig.inject(client_id="COGNITO_CLIENT_ID", pool_id="COGNITO_USER_POOL_ID")
    def login_user(self, username, password, client_id=None, pool_id=None) -> str:
        secret_hash = AuthenticationService._build_secret_hash(username)
        client = AuthenticationService._cognito_client()
        resp = client.admin_initiate_auth(
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash,
            },
            ClientId=client_id,
            UserPoolId=pool_id,
        )

        id_token = resp["AuthenticationResult"]["IdToken"]
        claims = AuthenticationService._parse_jwt_token(id_token)
        return AuthenticationService._save_login(
            claims["sub"],
            claims["email"],
            resp["AuthenticationResult"]["AccessToken"],
            resp["AuthenticationResult"]["RefreshToken"],
        )

    @GlobalConfig.inject(client_id="COGNITO_CLIENT_ID")
    def register_user(self, email, password, client_id=None) -> Dict:
        secret_hash = self._build_secret_hash(email)
        client = self._cognito_client()
        resp = client.sign_up(
            ClientId=client_id,
            SecretHash=secret_hash,
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        account, _ = self._get_or_create_account(resp["UserSub"], email)
        return account

    def _save_login(
        self, cognito_id: UUID, email: str, access_token: str, refresh_token: str
    ) -> str:
        account, _ = self._get_or_create_account(cognito_id, email)
        return self._create_token(account["id"], access_token, refresh_token)

    @GlobalConfig.inject(client_id="COGNITO_CLIENT_ID")
    def _parse_jwt_token(self, token, client_id: str = None):
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
        key = AuthenticationService._jwks_json()[kid]
        return jwt.decode(token, key, audience=client_id)

    @GlobalConfig.inject(
        client_id="COGNITO_CLIENT_ID", client_secret="COGNITO_CLIENT_SECRET"
    )
    def _build_secret_hash(
        self, username: str, client_id: str = "", client_secret: str = ""
    ) -> str:
        to_digest = f"{username}{client_id}"
        digest = hmac.new(
            client_secret.encode("utf-8"),
            msg=to_digest.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        return base64.b64encode(digest).decode()

    @cache_region(LOCAL_LONG_TERM, "_cognito_client")
    @GlobalConfig.inject(region="AWS_REGION")
    def _cognito_client(self, region: str = None):
        return boto3.client("cognito-idp", region_name=region)

    @cache_region(LOCAL_LONG_TERM, "_cognito_jwks")
    @GlobalConfig.inject(jwks_file="COGNITO_JWKS_FILE")
    def _jwks_json(self, jwks_file: str = ""):
        with open(jwks_file) as jwks_json:
            json_data = rapidjson.load(jwks_json)
        return {data["kid"]: data for data in json_data["keys"]}

    def _get_or_create_account(self, cognito_id: UUID, email: str) -> Tuple[Dict, bool]:
        try:
            return AuthenticationDAO.get_account_for_cognito_id(cognito_id), False
        except SQLNotFoundException:
            LOG.info(
                'Creating a new account because a row was not found for "%s"',
                cognito_id,
            )
            self.authentication_dao.create_account(
                Role.default.value, email, cognito_id
            )
            return AuthenticationDAO.get_account_for_cognito_id(cognito_id), True

    def _create_token(
        self,
        account_id: UUID,
        access_token: str,
        refresh_token: str,
        expiration: float = None,
    ) -> str:
        if expiration is None:
            expiration = GlobalConfig.config["DEFAULT_TOKEN_EXPIRATION_SECONDS"]
        expiration_time = datetime.utcnow() + timedelta(
            seconds=expiration
        )  # type: ignore
        return self.authentication_dao.create_token(
            account_id, access_token, refresh_token, expiration_time
        )

    def logout_account(self, token: str):
        self.authentication_dao.delete_token(token)

    def get_account_by_token(self, token: str) -> UUID:
        try:
            return self.authentication_dao.get_account_for_token(token)
        except SQLNotFoundException as exc:
            raise NotLoggedInException from exc
