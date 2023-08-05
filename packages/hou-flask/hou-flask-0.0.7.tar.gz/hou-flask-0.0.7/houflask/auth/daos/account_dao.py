from typing import List
from uuid import UUID

from hou_flask_psycopg2 import Psycopg2Utils

from houflask.auth.daos.authentication_dao import Username, Account


class AccountDAO:
    db: Psycopg2Utils

    def __init__(self, db: Psycopg2Utils):
        self.db = db

    def get_username(self, user_id: UUID) -> Username:
        query = """
        SELECT email AS username, id AS account_id
        FROM account
        WHERE id = %s
        """
        return self.db.execute_query_conversion(
            query, (user_id,), Username, expect_one=True
        )

    def get_usernames(
        self, name_filter: str, page: int, page_size: int
    ) -> List[Username]:
        query = """
        SELECT email AS username, id AS account_id
        FROM account
        WHERE email ILIKE %s ESCAPE '='
        ORDER BY LOWER(email)
        LIMIT %s
        OFFSET %s
        """
        name_filter = self.db.unsafe_escape_like_string(
            name_filter, escape_character="="
        )
        return self.db.execute_query_conversion(
            query, (f"%{name_filter}%", page_size, page_size * page), Username
        )

    def get_account_info(self, account_id: UUID) -> Account:
        query = """
        SELECT email AS username, id
        FROM account
        WHERE id = %s
        """
        return self.db.execute_query_conversion(
            query, (account_id,), Account, expect_one=True
        )
