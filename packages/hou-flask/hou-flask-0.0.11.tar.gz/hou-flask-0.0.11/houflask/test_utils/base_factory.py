import copy
import random
from collections import namedtuple
from enum import Enum
from string import ascii_letters
from typing import Dict, Iterable, List

from factory import Factory
from hou_flask_psycopg2 import Psycopg2Utils
from psycopg2.extras import DictCursor
from psycopg2.sql import SQL, Identifier


def random_string(length=10):
    return "".join(random.choice(ascii_letters) for _ in range(length))


def random_email(length=10):
    # This format doesn't cause AWS to censure us
    # They accept these but they don't actually send an email I believe
    return "success+{}@simulator.amazonses.com".format(random_string(length))


class Model:
    def __init__(self, table_name: str, db: Psycopg2Utils):
        self.table = table_name
        self.db = db

    def __call__(self, **kwargs):
        model_class = namedtuple(self.table, kwargs.keys())
        return model_class(**kwargs)


class EmptyRelationship:
    def __getattr__(self, item):
        return None


_RELATIONSHIP_TYPES = (tuple, EmptyRelationship, Enum)


class BaseFactory(Factory):
    # pylint: disable=arguments-differ
    @classmethod
    def _build(cls, model_class, **kwargs):
        relationships = {
            k: v for k, v in kwargs.items() if isinstance(v, _RELATIONSHIP_TYPES)
        }
        real_values = {
            k: v for k, v in kwargs.items() if not isinstance(v, _RELATIONSHIP_TYPES)
        }
        keys = ["{{{}}}".format(k) for k in real_values.keys()]
        values = ", ".join(["%({})s".format(k) for k in real_values.keys()])
        identifiers = {k: Identifier(k) for k in real_values.keys()}
        query = SQL(
            """
        INSERT INTO {{table_name}} ({keys})
        VALUES ({values})
        RETURNING *
        """.format(
                keys=", ".join(keys), values=values
            )
        ).format(table_name=Identifier(model_class.table), **identifiers)
        resp = dict(
            model_class.db.execute_query(query, real_values, factory=DictCursor)[0]
        )
        resp.update(**relationships)
        model = model_class(**resp)
        return model

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._build(model_class, *args, **kwargs)

    @classmethod
    def build_batch(cls, *args, **kwargs):
        return super(BaseFactory, cls).build_batch(*args, **kwargs)

    @classmethod
    def build_distinct_batch(
        cls, distinct_kwargs: Iterable[Dict], **common_kwargs
    ) -> List:
        models = []
        for kwargs in distinct_kwargs:
            kwargs = copy.deepcopy(kwargs)
            kwargs.update(common_kwargs)
            models.append(cls.build(**kwargs))
        return models
