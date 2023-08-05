import secrets
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from uuid import UUID

from hou_flask_psycopg2 import SQLNotFoundException, Psycopg2Utils
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor

__all__ = ["AuthenticationDAO"]


@dataclass
class Account:
    username: str
    id: UUID


@dataclass(order=True, frozen=True, unsafe_hash=True)
class Username:
    account_id: UUID
    username: str


class AuthenticationDAO:
    db: Psycopg2Utils

    def __init__(self, db: Psycopg2Utils):
        self.db = db

    def get_account_for_cognito_id(self, cognito_id: UUID) -> Dict:
        return self.db.execute_query(
            """
            SELECT id, cognito_id
            FROM account
            WHERE cognito_id = %s
            """,
            (cognito_id,),
            factory=RealDictCursor,
            expect_one=True,
        )

    def create_account(self, role_name: str, email: str, cognito_id: UUID) -> UUID:
        try:
            return self.db.execute_query(
                """
                INSERT INTO account (role_name, email, cognito_id)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (role_name, email, cognito_id),
                expect_one=True,
            )[0]
        except IntegrityError as exc:
            raise SQLNotFoundException(f"Missing role: {role_name}") from exc

    def create_token(
        self,
        account_id: UUID,
        access_token: str,
        refresh_token: str,
        expiration: datetime,
    ) -> str:
        token = secrets.token_urlsafe(64)
        query = """
        INSERT INTO token (
          account_id, 
          token,
          expiry,
          cognito_access_token,
          cognito_refresh_token
        )
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute_query_without_fetch(
            query, (account_id, token, expiration, access_token, refresh_token)
        )
        return token

    def get_account_for_token(self, token: str) -> UUID:
        account_ids = self.db.execute_query(
            """
            SELECT account_id
            FROM token
            WHERE token = %s
            """,
            (token,),
        )
        if not account_ids:
            raise SQLNotFoundException("User not logged in")
        return account_ids[0][0]

    def delete_token(self, token: str) -> None:
        query = """
        DELETE FROM token
        WHERE token.token = %s
        """
        self.db.execute_query_without_fetch(query, (token,))
