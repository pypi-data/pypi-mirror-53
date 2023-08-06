from __future__ import annotations

from typing import Any, Union, TYPE_CHECKING
import copy

import sqlalchemy as alch
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from maybe import Maybe
from subtypes import Str
from miscutils import NameSpace, Cache

from .custom import Model

if TYPE_CHECKING:
    from .sql import Sql


class Database:
    def __init__(self, sql: Sql) -> None:
        self.sql, self.name, self.cache = sql, sql.engine.url.database, Cache(file=sql.config.appdata.newfile("sql_cache", "pkl"), days=5)
        self.meta = self._get_metadata()
        self.declaration = self.reflection = None  # type: Model
        self.orm, self.objects = Schemas(database=self), Schemas(database=self)
        self.default_schema_name = vars(self.sql.engine.dialect).get("schema_name", "default")

        self._refresh_declarative_base()
        for schema in {self.meta.tables[table].schema for table in self.meta.tables}:
            self._add_schema_to_namespaces(schema)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={repr(self.name)}, orm={repr(self.orm)}, objects={repr(self.objects)}, cache={repr(self.cache)})"

    def reflect(self, schema: str = None) -> None:
        schema = None if schema == self.default_schema_name else schema

        self.meta.reflect(schema=schema, views=True)
        self._refresh_declarative_base()
        self._add_schema_to_namespaces(schema)

        self.cache[self.name] = self.meta

    def create_table(self, table: alch.schema.Table) -> None:
        table = self._normalize_table(table)
        table.create()
        self.reflect(table.schema)

    def drop_table(self, table: alch.schema.Table) -> None:
        table = self._normalize_table(table)
        table.drop()

        self.meta.remove(table)
        del self.orm[table.schema][table.name]
        del self.objects[table.schema][table.name]

        self.cache[self.name] = self.meta

    def refresh_table(self, table: alch.schema.Table) -> None:
        table = self._normalize_table(table)

        self.meta.remove(table)
        del self.orm[table.schema][table.name]
        del self.objects[table.schema][table.name]

        self.reflect(table.schema)

    def clear(self) -> None:
        self.meta.clear()
        self.cache[self.name] = self.meta
        for namespace in (self.orm, self.objects):
            namespace._clear()

    def _refresh_declarative_base(self) -> None:
        self.declaration = declarative_base(bind=self.sql.engine, metadata=self.meta, cls=Model)
        self.declaration.sql = self.sql

    def _add_schema_to_namespaces(self, schema: str) -> None:
        schema = None if schema == self.default_schema_name else schema

        new_meta = copy.copy(self.meta)
        invalid_tables = ({table for table in new_meta.tables if new_meta.tables[table].schema is not None}
                          if schema is None else
                          {table for table in new_meta.tables if new_meta.tables[table].schema is None or new_meta.tables[table].schema.lower() != schema})

        for table in invalid_tables:
            new_meta.remove(new_meta.tables[table])

        declaration = declarative_base(bind=self.sql.engine, metadata=new_meta, cls=Model)
        declaration.sql = self.sql

        automap = automap_base(declarative_base=declaration)
        automap.prepare(name_for_collection_relationship=self._pluralize_collection)

        self.orm._add_schema(name=schema, tables=list(automap.classes))
        self.objects._add_schema(name=schema, tables=[new_meta.tables[item] for item in new_meta.tables])

    def _get_metadata(self) -> None:
        meta = self.cache.setdefault(self.name, alch.MetaData())
        meta.bind = self.sql.engine
        return meta

    def _normalize_table(self, table: Union[Model, alch.schema.Table]) -> alch.schema.Table:
        return Maybe(table).__table__.else_(table)

    @staticmethod
    def _pluralize_collection(base: Any, local_cls: Any, referred_cls: Any, constraint: Any) -> str:
        referred_name = referred_cls.__name__
        return str(Str(referred_name).case.snake().case.plural())


class Schemas(NameSpace):
    def __init__(self, database: Database) -> None:
        super().__init__()
        self._database = database

    def __repr__(self) -> str:
        return f"""{type(self).__name__}(num_schemas={len(self)}, schemas=[{", ".join([f"{type(schema).__name__}(name='{schema._name}', tables={len(schema)})" for name, schema in self])}])"""

    def __getitem__(self, name: str) -> Schema:
        return getattr(self, self._database.default_schema_name) if name is None else super().__getitem__(name)

    def __getattr__(self, attr: str) -> Schema:
        if not attr.startswith("_"):
            self._database.reflect(attr)

        try:
            return super().__getattribute__(attr)
        except AttributeError:
            raise AttributeError(f"{type(self._database).__name__} '{self._database.name}' has no schema '{attr}'.")

    def _add_schema(self, name: str, tables: list) -> None:
        name = Maybe(name).else_(self._database.default_schema_name)
        if name in self:
            self[name]._refresh_from_tables(tables)
        else:
            self[name] = Schema(database=self._database, name=name, tables=tables)


class Schema(NameSpace):
    def __init__(self, database: Database, name: str, tables: list) -> None:
        super().__init__({Maybe(table).__table__.else_(table).name: table for table in tables})
        self._database, self._name = database, name

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={repr(self._name)}, num_tables={len(self)}, tables={[table for table, _ in self]})"

    def __getattr__(self, attr: str) -> Model:
        if not attr.startswith("_"):
            self._database.reflect(self._name)

        try:
            return super().__getattribute__(attr)
        except AttributeError:
            raise AttributeError(f"{type(self).__name__} '{self._name}' of {type(self._database).__name__} '{self._database.name}' has no object '{attr}'.")

    def _refresh_from_tables(self, tables: list) -> None:
        self._clear()
        for name, table in {Maybe(table).__table__.else_(table).name: table for table in tables}.items():
            self[name] = table
