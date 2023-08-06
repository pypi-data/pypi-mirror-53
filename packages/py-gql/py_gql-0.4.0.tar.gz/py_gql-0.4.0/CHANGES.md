Changelog
=========

Unreleased
----------

[0.4.0](https://github.com/lirsacc/py-gql/releases/tag/0.4.0) - 2019-10-10
--------------------------------------------------------------------------

### Breaking Changes & Deprecations

- `py_gql.builders` has been moved to `py_gql.sdl` and `build_schema_ignoring_extensions` has been removed.
- `Tracer` has been replaced by the more general concept of `Instrumentation` which is now backing `ApolloTracer`.
- `Directive` is not a subclass of `GraphQLType` anymore.
- It is no longer possible to override specified directives and types when creating a schema.
- Dropped `is_abstract_type`, `is_composite_type` and `is_leaf_type`: use instance checks against `GraphQLAbstractType`, `GraphQLCompositeType`, and `GraphQLLeafType` directly instead.
- Dropped `ObjectType.is_type_of` option for concrete type resolution, use `(UnionType|InterfaceType).resolve_type` instead.

### Added

- Add support for `copy` and `deepcopy` to `py_gql.lang.ast.Node`.
- `py_gql.lang.Visitor` now supports modifying the nodes inline; this supports the implementation of some common AST transformers.
- Add `py_gql.utilities.ast_transforms.RemoveFieldAliasesVisitor` to canonicalise queries from a server's perspective.
- Add `py_gql.utilities.ast_transforms.CamelCaseToSnakeCaseVisitor` and `py_gql.utilities.ast_transforms.SnakeCaseToCamelCaseVisitor` to support interacting with common convetions in the wider GraphQL ecosystem.
- Extended the tracer concept into `Instrumentation` which supports overriding runtime values as well as observing execution stages.
- `(UnionType|InterfaceType).resolve_type` now receives the current resolution data value and `ResolveInfo`.
- Basic subscription support has been added through `py_gql.execution.subscribe`. It's not well documented yet is subject to change. For now refer to the _starlette-ws-subsriptions_ example.

### Fixed

- Fix a bug where selection set indentation was not correct when using `ASTPrinter`.
- Do not import `typing.Deque` outside of type checking context to ensure compatibility with versions `<= 3.5.3`.

[0.3.2](https://github.com/lirsacc/py-gql/releases/tag/0.3.2) - 2019-05-01
--------------------------------------------------------------------------

Docs & dev update.

[0.3.0](https://github.com/lirsacc/py-gql/releases/tag/0.3.0) - 2019-05-01
--------------------------------------------------------------------------

### Breaking Changes

- `AsyncExecutor` renamed to `AsyncIOExecutor`
- `allow_type_system` argument to `py_gql.lang.Parser` now defaults to `False`.
- `SchemaDirective` do not support defining their own definition which now has to be defined in the schema.
- `py_gql.utilities.diff_schema` has been moved to its own submodule `py_gql.utilities.diff_schema.diff_schema` (alongside related types and constants).
- `py_gql.utilities.diff_schema.diff_schema` now return instances of `SchemaChange` instead of combining enum values and formatted string in a tuple. The classes contain more context and references to the actual schema objects (Field, Argument, etc.).

### Updated

- Support passing an already parsed ast to `process_graphql_query` and its derivatives.
- `ASTSchemaPrinter` (and `Schema.to_string()`) now supports printing custom schema directives collected when using `build_schema` behind the `include_custom_directives` flag.

### Fixed

- Handle early return from `process_graphql_query` in `py_gql.graphql`.
- Make sure `process_graphql_query` calls `tracer.on_end()` on early returns.
- Fix link in the description of the `UUID` scalar type.
- Fix bug in `Executor.complete_value` which lead to incorrectly ignoring fragment when applied on types implementing an interface.

[0.2.0](https://github.com/lirsacc/py-gql/releases/tag/0.2.0) - 2019-04-18
--------------------------------------------------------------------------

This release follow some extensive internal refactor and legwork in order to make `py_gql` easier to improve and extend moving forward.

### Most notable changes

- **Dropped Python 2 support**; the minimum supported version is now Python 3.5.
- `py_gql.build_schema` is now the preferred way to define executable GraphQL schema (instead of using the `py_gql.schema.Schema` class).
- `py_gql.graphql` now defaults to working with `asyncio`. Use `py_gql.graphql_blocking` for synchronous use cases. This should make things more obvious when implementing subscriptions. `py_gql.process_graphql_query` is still available in order to support custom executors.
- Finalised implementation of schema directives for `py_gql.build_schema`.
- Resolvers can now be assigned with the `py_gql.schema.Schema.resolver` decorator.
- Added type hints for most exposed apis, however some types are still too open and this will be improved moving forward.
- Simplify middleware and tracer implementation: middlewares do not try to be smart and users have to write them against their resolver and executor. Tracers are not based on middlewares anymore.
- Many small performance improvements.
- Returning callables to lazily resolve values has been deprecated.?
- Fixed custom scalars support during execution.
- Updated some error messages to match the reference implementation more closely.
- Implementing custom `py_gql.execution.Executor` is a bit more involved in order to simplify the implementations of the execution layer.
- `py_gql.utilities.diff_schema` added to compare schemas for compatibility.

0.1.0
-----

Initial release.
