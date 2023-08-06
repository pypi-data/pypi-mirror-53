from logging import Logger

import rapidjson
from flask import Response, request, Flask
from hou_flask_psycopg2 import SQLNotFoundException
from ultra_config import GlobalConfig
from werkzeug.exceptions import HTTPException, default_exceptions

__all__ = ["FlaskErrorHandler"]


class FlaskErrorHandler:
    def __init__(self, logger: Logger):
        self.app = None
        self.login_url = None
        self.logger = logger

    def init_app(self, app: Flask, login_url: str) -> Flask:
        self.app = app
        self.login_url = login_url

        app.register_error_handler(
            SQLNotFoundException, self.handle_object_not_found_exception
        )
        app.register_error_handler(Exception, self.handle_generic_exception)
        for exception_type in default_exceptions.values():
            app.register_error_handler(exception_type, self.handle_http_exception)

        return app

    def handle_object_not_found_exception(
        self, exception: SQLNotFoundException
    ) -> Response:
        self._log_exception(exception, verbose=False)
        return self._build_error_response(
            status_code=404,
            message="The requested object either does not "
            "exist or you do not have access to it",
            error_class="ResourceNotFoundException",
        )

    def handle_generic_exception(self, exception: Exception) -> Response:
        """
        The base exception handler for arbitrary exceptions
        Returns 500 errors with no information to avoid security issues
        """
        self._log_exception(exception)
        return self._build_error_response()

    def handle_http_exception(self, exception: HTTPException):
        """
        Handle HTTPExceptions from werkzeug
        """
        status_code = getattr(exception, "code", 500)
        if status_code >= 500:
            self._log_exception(exception)
            return self._build_error_response(status_code=status_code)
        if status_code < 400:
            raise exception
        extra_params = {}
        if status_code == 401:
            extra_params["login_url"] = self.login_url

        self._log_exception(exception, verbose=False)
        return self._build_error_response(
            status_code=status_code,
            message=exception.description,
            error_class=self._get_exception_name(exception),
            **extra_params
        )

    @staticmethod
    def _build_error_response(
        status_code=500,
        message="An Error has Occurred",
        error_class="ServerError",
        **extra
    ):
        data = {"message": message, "error_type": error_class}
        data.update(extra)
        return Response(
            rapidjson.dumps(data), status=status_code, content_type="application/json"
        )

    @staticmethod
    def _get_exception_name(exception: Exception):
        if hasattr(exception, "name"):
            return exception.name
        return exception.__class__.__name__

    def _log_exception(self, exception: Exception, verbose=True):
        if verbose or GlobalConfig.config["VERBOSE_4XX_ERROR_LOGGING"]:
            self.logger.exception(exception)
        exception_name = self._get_exception_name(exception)
        self.logger.warning(
            'Failing on route "%s": %s\nHeaders: %s\nBody: %s',
            request.url,
            exception_name,
            request.headers,
            request.get_data(),
        )
