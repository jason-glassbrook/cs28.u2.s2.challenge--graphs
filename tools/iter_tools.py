############################################################

import typing as ty
from itertools import chain
from copy import copy

############################################################
#   Type Checking
############################################################


def is_iterable(thing) -> bool:
    return isinstance(thing, ty.Iterable)


############################################################
#   Joining
############################################################


def join_as(
    cast: ty.Callable[[ty.Iterable], ty.Iterable],
    *iters: ty.Iterable[ty.Iterable],
) -> ty.Iterable:

    return cast(chain(*iters))


def join_as_list(*iters: ty.Iterable[ty.Iterable]) -> list:

    return join_as(list, *iters)


def join_as_tuple(*iters: ty.Iterable[ty.Iterable]) -> tuple:

    return join_as(tuple, *iters)


def join_as_set(*iters: ty.Iterable[ty.Iterable]) -> set:

    return join_as(set, *iters)


############################################################
#   Keys
############################################################


def keys_as(
    cast: ty.Callable[[ty.Iterable], ty.Iterable],
    mapping: ty.Mapping,
) -> ty.Iterable:

    return cast(mapping.keys())


def keys_as_list(mapping: ty.Mapping) -> list:

    return keys_as(list, mapping)


def keys_as_tuple(mapping: ty.Mapping) -> tuple:

    return keys_as(tuple, mapping)


def keys_as_set(mapping: ty.Mapping) -> set:

    return keys_as(set, mapping)


############################################################
#   Building Collections
############################################################


def inherit(
    family: ty.Mapping,
    member_key: ty.Any,
    overlay: ty.Optional[ty.Mapping] = None,
    underlay: ty.Optional[ty.Mapping] = None,
    extends_key: str = "extends",
    delete_extends_key: bool = False,
) -> ty.Dict:

    overlay = copy(overlay) if overlay is not None else dict()
    filling = dict()
    underlay = copy(underlay) if underlay is not None else dict()

    while member_key is not None and member_key in family:

        member = family[member_key]
        member_extends = member[extends_key] if extends_key in member else None

        filling = {
            **copy(member),
            **filling,
            "extends": member_extends,
        }

        member_key = member_extends

    if delete_extends_key and extends_key in filling:
        del filling[extends_key]

    result = {
        **underlay,
        **filling,
        **overlay,
    }

    return result


############################################################
#   Stringifying
############################################################

ty__iter_to_str__style = ty.Mapping[str, ty.Any]
ty__iter_to_str__style__to_str = ty.Callable[[ty.Iterable, ty.Any, int], str]

ITER_TO_STR__STYLE_FAMILY = {
    "base": {
        "extends": None,
        "to_str": (lambda i, x, c: repr(x)),
        "before_all": "",
        "after_all": "",
        "between": ", ",
        "before_each": "",
        "after_each": "",
    },
    "plain": {
        "extends": "base",
        "to_str": (lambda i, x, c: str(x)),
    },
    "tuple": {
        "extends": "base",
        "before_all": "(",
        "after_all": ")",
    },
    "list": {
        "extends": "base",
        "before_all": "[",
        "after_all": "]",
    },
    "set": {
        "extends": "base",
        "before_all": "{",
        "after_all": "}",
    },
    "dict": {
        "extends": "set",
        "to_str": (lambda i, x, c: f"{repr(x)}: {repr(c[x])}"),
    },
    "args": {
        "extends": "base",
    },
    "kwargs": {
        "extends": "args",
        "to_str": (lambda i, x, c: f"{str(x)}={repr(c[x])}"),
    },
}

ITER_TO_STR__STYLES = {
    key: inherit(ITER_TO_STR__STYLE_FAMILY, key, delete_extends_key=True)
    for key in ITER_TO_STR__STYLE_FAMILY.keys()
}


def iter_to_str(
    c: ty.Iterable[ty.Any],
    style: ty.Union[None, str, ty__iter_to_str__style] = None,
    **options,
) -> str:

    # Parse `style`

    style_name = None
    style_dict = None

    if style is None:

        style_name = "base"

    elif isinstance(style, str):
        if style in ITER_TO_STR__STYLES:

            style_name = style

        else:
            raise Exception("iter_to_str.UnknownStyleError")

    elif isinstance(style, ty.Mapping):

        style_dict = style

    else:
        raise Exception("iter_to_str.InvalidStyleError")

    # Check `options` for valid `to_str`

    if "to_str" in options:
        if not isinstance(options["to_str"], ty.Callable):
            raise Exception("iter_to_str.InvalidStyleError.to_str")

    # Combine `style` with `options`

    if style_name is not None:
        style = inherit(ITER_TO_STR__STYLES, style_name)

    elif style_dict is not None:
        style = inherit(ITER_TO_STR__STYLES, "base", overlay=style_dict)

    else:
        raise Exception("iter_to_str.ProgrammerError")

    if "extends" in style:
        style = inherit(
            ITER_TO_STR__STYLES,
            style["extends"],
            overlay=style,
            delete_extends_key=True,
        )

    if "extends" in options:
        options = inherit(
            ITER_TO_STR__STYLES,
            options["extends"],
            overlay=options,
            delete_extends_key=True,
        )

    style = {
        **style,
        **options,
    }

    # Style the iterable `iter`

    def each_str(i: ty.Any, x: ty.Any, c: ty.Iterable) -> str:
        return "".join((
            style["before_each"],
            style["to_str"](i, x, c),
            style["after_each"],
        ))

    def all_str() -> str:
        return "".join((
            style["before_all"],
            style["between"].join(each_str(i, x, c) for (i, x) in enumerate(c)),
            style["after_all"],
        ))

    return all_str()
