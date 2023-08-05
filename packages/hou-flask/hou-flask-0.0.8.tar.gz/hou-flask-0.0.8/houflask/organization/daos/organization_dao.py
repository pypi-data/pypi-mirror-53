from dataclasses import dataclass
from typing import List, Set
from uuid import UUID

from hou_flask_psycopg2 import Psycopg2Utils
from psycopg2 import IntegrityError
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2.extras import DictCursor

from ...exceptions import OrganizationNameUnavailable, OrganizationNotFound


@dataclass
class Organization:
    name: str
    id: UUID
    active: bool


class OrganizationDAO:
    db: Psycopg2Utils

    def __init__(self, db: Psycopg2Utils):
        self.db = db

    def create(self, name: str, active: bool = True) -> Organization:
        query = """
        INSERT INTO organization (name, active)
        VALUES (%(name)s, %(active)s)
        RETURNING id, name, active
        """
        try:
            rows = self.db.execute_query(
                query, {"name": name, "active": active}, factory=DictCursor
            )
        except IntegrityError as exc:
            if exc.pgcode == UNIQUE_VIOLATION:
                raise OrganizationNameUnavailable(
                    f'The organization name "{name}" is unavailable'
                ) from exc
            raise exc
        # TODO: Remove type ignore when mypy actually supports dataclasses
        return Organization(**rows[0])  # type: ignore

    def update(self, id_: UUID, name: str, active: bool) -> Organization:
        query = """
        UPDATE organization
        SET name = %(name)s,
            active = %(active)s
        WHERE id = %(id)s
        RETURNING id, name, active
        """
        try:
            rows = self.db.execute_query(
                query, {"id": id_, "name": name, "active": active}, factory=DictCursor
            )
        except IntegrityError as exc:
            if exc.pgcode == UNIQUE_VIOLATION:
                raise OrganizationNameUnavailable(
                    f'The organization name "{name}" is unavailable'
                ) from exc
            raise exc
        else:
            if not rows:
                raise OrganizationNotFound(id_)
            # TODO: Remove type ignore when mypy actually supports dataclasses
            return Organization(**rows[0])  # type: ignore

    def get_orgs_for_account(self, account_id: UUID) -> List[Organization]:
        query = """
        SELECT name, id, active
        FROM organization AS o
        INNER JOIN organization_account AS oa
          ON oa.organization_id = o.id
        WHERE oa.account_id = %s
        """
        return self.db.execute_query_conversion(query, (account_id,), Organization)

    def get_all_orgs(
        self, page: int = 0, page_size: int = 100, name_filter: str = ""
    ) -> List[Organization]:
        """
        Get all orgs with a case insensitive match to the filter.
        By default returns all orgs.  Orgs, are sorted by name case
        insensitively. Pages are 0 indexed.
        """
        query = """
        SELECT name, id, active
        FROM organization
        WHERE name ILIKE %(filter)s ESCAPE '='
        ORDER BY LOWER(name)
        LIMIT %(page_size)s
        OFFSET %(offset)s
        """
        name_filter = self.db.unsafe_escape_like_string(name_filter)
        params = {
            "filter": f"%{name_filter}%",
            "page_size": page_size,
            "offset": page * page_size,
        }
        return self.db.execute_query_conversion(query, params, Organization)

    def get_orgs(self, org_ids: Set[UUID]) -> List[Organization]:
        if not org_ids:
            return []
        query = """
        SELECT name, id, active
        FROM organization
        WHERE id IN %s
        """
        rows = self.db.execute_query_conversion(query, (tuple(org_ids),), Organization)
        return self.db.verify_row_count(rows, len(org_ids))

    def get_org(self, organization_id: UUID) -> Organization:
        return self.get_orgs({organization_id})[0]

    def org_name_exists(self, name: str) -> bool:
        query = "SELECT 1 FROM organization WHERE name = %(name)s"
        return len(self.db.execute_query(query, {"name": name})) > 0
