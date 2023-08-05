import logging

from hou_flask_psycopg2 import Psycopg2Utils
from status_checker import StatusChecker
import os

from houflask.connexion import FlaskConnexionExtension
from houflask.http import json_response

LOG = logging.getLogger(__name__)


class _MetaView:
    db: Psycopg2Utils
    status_checker: StatusChecker
    app_version: str

    def init_app(
        self,
        db: Psycopg2Utils,
        connexion_app: FlaskConnexionExtension,
        app_version: str,
        **additional_checks
    ):
        self.db = db
        self.status_checker = StatusChecker(
            database=self._check_database, **additional_checks
        )
        self.app_version = app_version
        swagger_file = os.path.join(os.path.dirname(__file__), "..", "swagger-spec.yml")
        connexion_app.add_api(swagger_file, base_path="/v1/meta")

    # pylint: disable=broad-except
    def _check_database(self):
        """
        Checks if the database is available

        :return: Return a dictionary with at least
            a key 'available' corresponding to a boolean
        :rtype: dict{str:object}
        """
        try:
            with self.db.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchall()
        except Exception as exc:
            return {"available": False, "message": str(exc)}
        else:
            return {"available": True, "message": "ready"}


META_VIEW = _MetaView()


def status():
    """
    Gets the status of this service and its dependencies
    """
    status_dict = META_VIEW.status_checker.status()
    status_code = 200 if status_dict["failure_count"] == 0 else 500
    return json_response(status_dict, status_code)


def version():
    """
    Gets the version of this service
    """
    version_info = {"version": META_VIEW.app_version}
    return json_response(version_info)
