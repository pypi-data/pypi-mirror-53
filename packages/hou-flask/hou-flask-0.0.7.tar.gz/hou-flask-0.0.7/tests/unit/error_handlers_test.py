from logging import ERROR, WARNING

import pytest
from werkzeug.exceptions import HTTPException, ServiceUnavailable, UnprocessableEntity

from oss_auth.error_handlers import (
    _log_exception,
    handle_generic_exception,
    handle_http_exception,
)


class LogExceptionTest:
    def test_when_no_name__gets_class_name(self, log_capture, request_context):
        _log_exception(Exception("blah"))
        assert log_capture.records[1].args[1] == "Exception"

    def test_when_name__gets_name(self, log_capture, request_context):
        class Blah(Exception):
            name = "something"

        _log_exception(Blah("blah"))
        assert log_capture.records[1].args[1] == "something"

    def test_when_not_verbose__no_exception_log(self, log_capture, request_context):
        _log_exception(Exception("blah"), verbose=False)
        assert len(log_capture.records) == 1
        assert log_capture.records[0].levelno == WARNING

    def test_when_verbose__contains_exception_log(self, log_capture, request_context):
        _log_exception(Exception("blah"), verbose=True)
        assert len(log_capture.records) == 2
        assert log_capture.records[0].levelno == ERROR
        assert log_capture.records[1].levelno == WARNING


class HandleGenericExceptionTest:
    def test_when_valid__no_disclosed_info(self, request_context):
        resp = handle_generic_exception(Exception("blah"))
        assert resp.status_code == 500
        expected_response = {
            "message": "An Error has Occurred",
            "error_type": "ServerError",
        }
        assert resp.json == expected_response


class HandleHTTPExceptionTest:
    def test_when_5xx_exception__no_disclosed_info(self, request_context):
        resp = handle_http_exception(ServiceUnavailable("something something"))
        assert resp.status_code == ServiceUnavailable.code
        expected_response = {
            "message": "An Error has Occurred",
            "error_type": "ServerError",
        }
        assert resp.json == expected_response

    def test_when_4xx_exception__gives_reason(self, request_context):
        resp = handle_http_exception(UnprocessableEntity("something something"))
        assert resp.status_code == UnprocessableEntity.code
        expected_response = {
            "message": "something something",
            "error_type": "Unprocessable Entity",
        }
        assert resp.json == expected_response

    def test_when_3xx_exception__raises_exception(self, request_context):
        class Redirect(HTTPException):
            code = 302

        with pytest.raises(Redirect):
            handle_http_exception(Redirect("blah"))
