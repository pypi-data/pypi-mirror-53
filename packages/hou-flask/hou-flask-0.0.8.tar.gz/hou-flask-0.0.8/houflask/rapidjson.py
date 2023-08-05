import rapidjson


def monkeypatch_rapidjson():
    """
    Force rapidjson to always convert UUID and datetimes
    """
    _monkeypatch_dumps()
    _monkeypatch_loads()


def _monkeypatch_dumps():
    original_dumps = rapidjson.dumps

    def _dumps(
        *args, separators=None, cls=None, **kwargs
    ):  # pylint: disable=unused-argument
        return original_dumps(
            *args,
            uuid_mode=rapidjson.UM_CANONICAL,
            datetime_mode=rapidjson.DM_ISO8601,
            **kwargs
        )

    rapidjson.dumps = _dumps


def _monkeypatch_loads():
    original_loads = rapidjson.loads

    def _loads(
        *args, separators=None, cls=None, **kwargs
    ):  # pylint: disable=unused-argument
        return original_loads(
            *args,
            uuid_mode=rapidjson.UM_CANONICAL,
            datetime_mode=rapidjson.DM_ISO8601,
            **kwargs
        )

    rapidjson.loads = _loads
