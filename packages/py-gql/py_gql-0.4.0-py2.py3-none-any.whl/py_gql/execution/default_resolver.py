# -*- coding: utf-8 -*-

from collections.abc import Mapping
from typing import Any

from .wrappers import ResolveInfo


def default_resolver(
    # fmt: off
    root: Any,
    context: Any,
    info: ResolveInfo,
    __isinstance: Any = isinstance,
    __getattr: Any = getattr,
    __callable: Any = callable,
    __mapping_cls: Any = Mapping,
    **args: Any
    # fmt: on
) -> Any:
    """Default resolver used during query execution.

    This resolver looks up the value from the ``root`` in the
    following lookup order:

    - If ``root`` is a dict subcass:

        - If the field name is present and non callable, return it
        - If the field name is present and callable, return the result of
            calling it passing in ``(context, info, **args)``.

    - If ``root`` has an attribute corresponding to the field name:

        - If the attribute is non callable, return it
        - If the attribute is callable, treat it like a method and return the
            result of calling it passing in ``(context, info, **args)``.

    - Return ``None``.

    Args:
        root: Value of the resolved parent node.
        context: User provided context value.
        info (py_gql.execution.ResolveInfo): Resolution context.
        **args: Coerced field arguments.

    Returns:
        Resolved value.

    """
    field_name = info.field_definition.name

    field_value = (
        root.get(field_name, None)
        if __isinstance(root, __mapping_cls)
        else __getattr(root, field_name, None)
    )

    if __callable(field_value):
        return field_value(context, info, **args)
    else:
        return field_value
