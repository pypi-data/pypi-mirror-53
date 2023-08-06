# -*- coding: utf-8 -*-
"""
py_gql
~~~~~~

py_gql is a pure python implementation of the `GraphQL <https://graphql.org/>`_
query language for Python 3.5+.

The main :mod:`py_gql` package provides the minimum required to build GraphQL
schemas and execute queries against them while the relevant submodules allow
you to customize the library's behaviour or implement your own GraphQL layer
on top of :mod:`py_gql`.
"""

# flake8: noqa

from ._pkg import __version__  # isort:skip

from . import lang, schema, tracers, utilities
from ._graphql import graphql, graphql_blocking, process_graphql_query
from .execution import GraphQLExtension, GraphQLResult, ResolveInfo
from .sdl import build_schema

__all__ = (
    "__version__",
    "graphql",
    "graphql_blocking",
    "process_graphql_query",
    "GraphQLResult",
    "GraphQLExtension",
    "ResolveInfo",
    "build_schema",
)
