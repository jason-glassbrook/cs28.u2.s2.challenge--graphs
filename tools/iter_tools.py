############################################################

import typing as ty
import builtins
import itertools
import functools
import copy

from .data_structures import DefaultDict
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

    return cast(itertools.chain(*iters))


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
        cast: ty.Callable[[ty.Iterable], ty.Iterable], mapping: ty.Mapping
) -> ty.Iterable:

    return cast(mapping.keys())


def keys_as_list(mapping: ty.Mapping) -> list:

    return keys_as(list, mapping)


def keys_as_tuple(mapping: ty.Mapping) -> tuple:

    return keys_as(tuple, mapping)


def keys_as_set(mapping: ty.Mapping) -> set:

    return keys_as(set, mapping)


############################################################
#   Mapping
############################################################

__base__map = builtins.map
__base__accumulate = itertools.accumulate
__base__reduce = functools.reduce
__base__zip_shortest = builtins.zip
__base__zip_longest = itertools.zip_longest

_MAP__KWARGS = set()


def map(
        fun: ty.Callable[[ty.Any], ty.Any],
        iterable: ty.Iterable[ty.Any],
) -> ty.Any:

    return __base__map(fun, iterable)


_ACCUMULATE__KWARGS = {"initial", "cast"}


def accumulate(
        fun: ty.Callable[[ty.Any, ty.Any], ty.Any],
        iterable: ty.Iterable[ty.Any],
        initial: ty.Optional[ty.Any] = None,
) -> ty.Any:

    result = (
        __base__accumulate(iterable, fun)
        if initial is None else __base__accumulate(iterable, fun, initial)
    )

    return result


_REDUCE__KWARGS = {"initial"}


def reduce(
        fun: ty.Callable[[ty.Any, ty.Any], ty.Any],
        iterable: ty.Iterable[ty.Any],
        initial: ty.Optional[ty.Any] = None,
) -> ty.Any:

    return (
        __base__reduce(fun, iterable)
        if initial is None else __base__reduce(fun, iterable, initial)
    )


_ZIP_SHORTEST__KWARGS = set()


def zip_shortest(iterables: ty.Iterable[ty.Any]) -> ty.Iterable:

    return __base__zip_shortest(*iterables)


_ZIP_LONGEST__KWARGS = {"fill_value"}


def zip_longest(
        iterables: ty.Iterable[ty.Iterable],
        fill_value: ty.Optional[ty.Any] = None,
) -> ty.Iterable:

    return __base__zip_longest(*iterables, fillvalue=fill_value)


_ZIP__KWARGS = join_as_set(
    _ZIP_SHORTEST__KWARGS,
    _ZIP_LONGEST__KWARGS,
    {"longest"},
)


def zip(
        iterables: ty.Iterable[ty.Iterable],
        longest: bool = False,
        fill_value: ty.Optional[ty.Any] = None,
) -> ty.Iterable:

    return (
        zip_longest(iterables, fill_value=fill_value)
        if longest else zip_shortest(iterables)
    )


_MAP_ZIPPED__KWARGS = join_as_set(
    _MAP__KWARGS,
    _ZIP__KWARGS,
)


def map_zipped(
        fun: ty.Callable[[ty.Any], ty.Any],
        iterables: ty.Iterable[ty.Iterable],
        **kwargs: ty.Mapping[str, ty.Any],
) -> ty.Iterable:

    kwargs = DefaultDict.OfValue(None, **kwargs)
    map__kwargs = {key: kwargs[key] for key in _MAP__KWARGS}
    zip__kwargs = {key: kwargs[key] for key in _ZIP__KWARGS}

    return map(fun, zip(iterables, **zip__kwargs), **map__kwargs)


_ACCUMULATE_ZIPPED__KWARGS = join_as_set(
    _MAP_ZIPPED__KWARGS,
    _ACCUMULATE__KWARGS,
)


def accumulate_zipped(
        fun: ty.Callable[[ty.Any, ty.Any], ty.Any],
        iterables: ty.Iterable[ty.Any],
        **kwargs: ty.Mapping[str, ty.Any],
) -> ty.Iterable:

    kwargs = DefaultDict.OfValue(None, **kwargs)
    map_zipped__kwargs = {key: kwargs[key] for key in _MAP_ZIPPED__KWARGS}
    accumulate__kwargs = {key: kwargs[key] for key in _ACCUMULATE__KWARGS}

    return map_zipped(
        lambda x: accumulate(fun, x, **accumulate__kwargs),
        iterables,
        **map_zipped__kwargs,
    )


_REDUCE_ZIPPED__KWARGS = join_as_set(
    _MAP_ZIPPED__KWARGS,
    _REDUCE__KWARGS,
)


def reduce_zipped(
        fun: ty.Callable[[ty.Any, ty.Any], ty.Any],
        iterables: ty.Iterable[ty.Any],
        **kwargs: ty.Mapping[str, ty.Any],
) -> ty.Iterable:

    kwargs = DefaultDict.OfValue(None, **kwargs)
    map_zipped__kwargs = {key: kwargs[key] for key in _MAP_ZIPPED__KWARGS}
    reduce__kwargs = {key: kwargs[key] for key in _REDUCE__KWARGS}

    return map_zipped(
        lambda x: reduce(fun, x, **reduce__kwargs),
        iterables,
        **map_zipped__kwargs,
    )


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

    overlay = copy.copy(overlay) if overlay is not None else dict()
    filling = dict()
    underlay = copy.copy(underlay) if underlay is not None else dict()

    while member_key is not None and member_key in family:

        member = family[member_key]
        member_extends = member[extends_key] if extends_key in member else None

        filling = {
            **copy.copy(member),
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

ty__iterable_to_str__style = ty.Mapping[str, ty.Any]
ty__iterable_to_str__style__to_str = ty.Callable[[ty.Iterable, ty.Any, int], str]

_ITERABLE_TO_STR__STYLE_FAMILY = {
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

_ITERABLE_TO_STR__STYLES = {
    key: inherit(_ITERABLE_TO_STR__STYLE_FAMILY, key, delete_extends_key=True)
    for key in _ITERABLE_TO_STR__STYLE_FAMILY.keys()
}


def iterable_to_str(
        iterable: ty.Iterable[ty.Any],
        style: ty.Union[None, str, ty__iterable_to_str__style] = None,
        **options
) -> str:

    # Parse `style`

    style_name = None
    style_dict = None

    if style is None:

        style_name = "base"

    elif isinstance(style, str):
        if style in _ITERABLE_TO_STR__STYLES:

            style_name = style

        else:
            raise Exception("iterable_to_str.UnknownStyleError")

    elif isinstance(style, ty.Mapping):

        style_dict = style

    else:
        raise Exception("iterable_to_str.InvalidStyleError")

    # Check `options` for valid `to_str`

    if "to_str" in options:
        if not isinstance(options["to_str"], ty.Callable):
            raise Exception("iterable_to_str.InvalidStyleError.to_str")

    # Combine `style` with `options`

    if style_name is not None:
        style = inherit(_ITERABLE_TO_STR__STYLES, style_name)

    elif style_dict is not None:
        style = inherit(_ITERABLE_TO_STR__STYLES, "base", overlay=style_dict)

    else:
        raise Exception("iterable_to_str.ProgrammerError")

    if "extends" in style:
        style = inherit(
            _ITERABLE_TO_STR__STYLES,
            style["extends"],
            overlay=style,
            delete_extends_key=True,
        )

    if "extends" in options:
        options = inherit(
            _ITERABLE_TO_STR__STYLES,
            options["extends"],
            overlay=options,
            delete_extends_key=True,
        )

    style = {
        **style,
        **options,
    }

    # Style the iterable `iterable`

    def each_str(i: ty.Any, x: ty.Any, c: ty.Iterable) -> str:
        return "".join((
            style["before_each"],
            style["to_str"](i, x, c),
            style["after_each"],
        ))

    def all_str() -> str:
        return "".join((
            style["before_all"],
            style["between"].join(
                each_str(i, x, iterable) for (i, x) in enumerate(iterable)
            ),
            style["after_all"],
        ))

    return all_str()
