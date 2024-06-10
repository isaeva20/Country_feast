"""Module for test runner."""

from typing import Any
from types import MethodType
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner
from django.db import connections


def prepare_db(self):
    """
    Prepares the database schema for testing.
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS states;')

class PostgresSchemaRunner(DiscoverRunner):
    """
    A custom DiscoverRunner for Django that prepares the database schema before running tests.
    """
    def setup_databases(self, **kwargs: Any) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """
        Sets up the databases for testing, including schema preparation.
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
