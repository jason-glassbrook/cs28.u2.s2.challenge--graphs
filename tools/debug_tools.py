############################################################
#   DEBUG TOOLS
############################################################

import typing as ty
from tools.data_structures import DefaultDict
from tools.iter_tools import iterable_to_str

############################################################

ty__name = str
ty__args = ty.Iterable[ty.Any]
ty__kwargs = ty.Mapping[str, ty.Any]
ty__messages = ty.Iterable[ty.Any]
ty__options = ty.Mapping[str, ty.Any]

############################################################
#   Parse Options
############################################################


def parse_options(**kwargs) -> ty__options:

    options = DefaultDict(lambda: None)

    options["call_sign"] = parse_options__call_sign(options, **kwargs)
    options["call_sign"]["name"] = parse_options__call_sign__name(options, **kwargs)
    options["call_sign"]["args"] = parse_options__call_sign__args(options, **kwargs)
    options["args"] = parse_options__args(options, **kwargs)
    options["kwargs"] = parse_options__kwargs(options, **kwargs)
    options["messages"] = parse_options__messages(options, **kwargs)

    return options


#-----------------------------------------------------------

DEFAULT__CALL_SIGN__BEFORE = "========================================\n"
DEFAULT__CALL_SIGN__AFTER = "\n----------------------------------------"


def parse_options__call_sign(
    #
        pre_options: ty.Optional[ty__options] = None,
    #
        call_sign__before: str = DEFAULT__CALL_SIGN__BEFORE,
        call_sign__after: str = DEFAULT__CALL_SIGN__AFTER,
    #
        **rest,
) -> ty__options:

    return {
        "before": call_sign__before,
        "after": call_sign__after,
    }


#-----------------------------------------------------------

DEFAULT__CALL_SIGN__NAME__BEFORE = ""
DEFAULT__CALL_SIGN__NAME__AFTER = ""


def parse_options__call_sign__name(
    #
        pre_options: ty.Optional[ty__options] = None,
    #
        call_sign__name__before: str = DEFAULT__CALL_SIGN__NAME__BEFORE,
        call_sign__name__after: str = DEFAULT__CALL_SIGN__NAME__AFTER,
    #
        **rest,
) -> ty__options:

    return {
        "before": call_sign__name__before,
        "after": call_sign__name__after,
    }


#-----------------------------------------------------------

DEFAULT__CALL_SIGN__ARGS__BEFORE = "("
DEFAULT__CALL_SIGN__ARGS__AFTER = ")"


def parse_options__call_sign__args(
    #
        pre_options: ty.Optional[ty__options] = None,
    #
        call_sign__args__before: str = DEFAULT__CALL_SIGN__ARGS__BEFORE,
        call_sign__args__after: str = DEFAULT__CALL_SIGN__ARGS__AFTER,
    #
        **rest,
) -> ty__options:

    return {
        "before": call_sign__args__before,
        "after": call_sign__args__after,
    }


#-----------------------------------------------------------

DEFAULT__ARGS__BEFORE_ALL = ""
DEFAULT__ARGS__AFTER_ALL = ""
DEFAULT__ARGS__BETWEEN = ", "
DEFAULT__ARGS__BEFORE_EACH = ""
DEFAULT__ARGS__AFTER_EACH = ""


def parse_options__args(
    #
        pre_options: ty.Optional[ty__options] = None,
    #
        args__before_all: str = DEFAULT__ARGS__BEFORE_ALL,
        args__after_all: str = DEFAULT__ARGS__AFTER_ALL,
        args__between: str = DEFAULT__ARGS__BETWEEN,
        args__before_each: str = DEFAULT__ARGS__BEFORE_EACH,
        args__after_each: str = DEFAULT__ARGS__AFTER_EACH,
    #
        **rest,
) -> ty__options:

    return {
        "before_all": args__before_all,
        "after_all": args__after_all,
        "between": args__between,
        "before_each": args__before_each,
        "after_each": args__after_each,
    }


#-----------------------------------------------------------

DEFAULT__KWARGS__BEFORE_ALL = None
DEFAULT__KWARGS__AFTER_ALL = None
DEFAULT__KWARGS__BETWEEN = None
DEFAULT__KWARGS__BEFORE_EACH = None
DEFAULT__KWARGS__AFTER_EACH = None


def parse_options__kwargs(
    #
        pre_options: ty.Optional[ty__options] = None,
    #
        kwargs__before_all: ty.Optional[str] = DEFAULT__KWARGS__BEFORE_ALL,
        kwargs__after_all: ty.Optional[str] = DEFAULT__KWARGS__AFTER_ALL,
        kwargs__between: ty.Optional[str] = DEFAULT__KWARGS__BETWEEN,
        kwargs__before_each: ty.Optional[str] = DEFAULT__KWARGS__BEFORE_EACH,
        kwargs__after_each: ty.Optional[str] = DEFAULT__KWARGS__AFTER_EACH,
    #
        **rest,
) -> ty__options:

    if pre_options is None:
        pre_options = {"args": parse_options__args(**rest)}

    return {
        "before_all": (
            kwargs__before_all
            if kwargs__before_all is not None else pre_options["args"]["before_all"]
        ),
        "after_all": (
            kwargs__after_all
            if kwargs__after_all is not None else pre_options["args"]["after_all"]
        ),
        "between": (
            kwargs__between
            if kwargs__between is not None else pre_options["args"]["between"]
        ),
        "before_each": (
            kwargs__before_each
            if kwargs__before_each is not None else pre_options["args"]["before_each"]
        ),
        "after_each": (
            kwargs__after_each
            if kwargs__after_each is not None else pre_options["args"]["after_each"]
        ),
    }


#-----------------------------------------------------------

DEFAULT__MESSAGES__BEFORE_ALL = ""
DEFAULT__MESSAGES__AFTER_ALL = ""
DEFAULT__MESSAGES__BETWEEN = ""
DEFAULT__MESSAGES__BEFORE_EACH = "\n... "
DEFAULT__MESSAGES__AFTER_EACH = ""


def parse_options__messages(
    #
        pre_options: ty.Optional[ty__options] = None,
    #
        messages__before_all: str = DEFAULT__MESSAGES__BEFORE_ALL,
        messages__after_all: str = DEFAULT__MESSAGES__AFTER_ALL,
        messages__between: str = DEFAULT__MESSAGES__BETWEEN,
        messages__before_each: str = DEFAULT__MESSAGES__BEFORE_EACH,
        messages__after_each: str = DEFAULT__MESSAGES__AFTER_EACH,
    #
        **rest,
) -> ty__options:

    return {
        "before_all": messages__before_all,
        "after_all": messages__after_all,
        "between": messages__between,
        "before_each": messages__before_each,
        "after_each": messages__after_each,
    }


############################################################
#   Debug Strings
############################################################


def debug_str(
        name: ty__name,
        args: ty.Optional[ty__args] = None,
        kwargs: ty.Optional[ty__kwargs] = None,
        messages: ty.Optional[ty__messages] = None,
        **options,
) -> str:

    return "".join((
        debug_str__call_sign(name, args, kwargs, **options),
        debug_str__messages(messages, **options),
    ))


#-----------------------------------------------------------


def debug_str__call_sign(
        name: ty__name,
        args: ty.Optional[ty__args] = None,
        kwargs: ty.Optional[ty__kwargs] = None,
        **options,
) -> str:

    o = parse_options__call_sign(**options)

    return "".join((
        o["before"],
        debug_str__call_sign__name(name, **options),
        debug_str__call_sign__args(args, kwargs, **options),
        o["after"],
    ))


#-----------------------------------------------------------


def debug_str__call_sign__name(
        name: ty.Optional[ty__name] = None,
        **options,
) -> str:

    o = parse_options__call_sign__name(**options)

    return "".join((
        o["before"],
        name,
        o["after"],
    ))


#-----------------------------------------------------------


def debug_str__call_sign__args(
        args: ty.Optional[ty__args] = None,
        kwargs: ty.Optional[ty__kwargs] = None,
        **options,
) -> str:

    o = parse_options__call_sign__args(**options)

    args_str = None

    if args is None and kwargs is None:
        args_str = ""

    elif args is not None and kwargs is None:
        args_str = debug_str__args(args, **options)

    elif args is None and kwargs is not None:
        args_str = debug_str__kwargs(kwargs, **options)

    else:
        args_str = iterable_to_str(
            (
                debug_str__args(args, **options),
                debug_str__kwargs(kwargs, **options),
            ),
            style="plain",
            **parse_options__args(**options),
        )

    return "".join((
        o["before"],
        args_str,
        o["after"],
    ))


#-----------------------------------------------------------


def debug_str__args(
        args: ty.Optional[ty__args] = None,
        **options,
) -> str:

    if args is None:
        return ""

    else:
        return iterable_to_str(
            args,
            style="args",
            **parse_options__args(**options),
        )


#-----------------------------------------------------------


def debug_str__kwargs(
        kwargs: ty.Optional[ty__kwargs] = None,
        **options,
) -> str:

    if kwargs is None:
        return ""

    else:
        return iterable_to_str(
            kwargs,
            style="kwargs",
            **parse_options__kwargs(**options),
        )


#-----------------------------------------------------------


def debug_str__messages(
        messages: ty.Optional[ty__messages] = None,
        **options,
) -> str:

    if messages is None:
        return ""

    else:
        return iterable_to_str(
            messages,
            style="plain",
            **parse_options__messages(**options),
        )


############################################################
#   Debug Prints
############################################################

DEFAULT__SHOULD_PRINT = True


def debug_print(
        name: ty__name,
        args: ty.Optional[ty__args] = None,
        kwargs: ty.Optional[ty__kwargs] = None,
        messages: ty.Optional[ty__messages] = None,
        should_print: bool = DEFAULT__SHOULD_PRINT,
        **options,
) -> None:

    if should_print:
        print(debug_str(name, args, kwargs, messages, **options))

    return


#-----------------------------------------------------------


def debug_print__call_sign(
    name: ty__name,
    args: ty.Optional[ty__args] = None,
    kwargs: ty.Optional[ty__kwargs] = None,
    should_print: bool = DEFAULT__SHOULD_PRINT,
    **options,
):

    if should_print:
        print(debug_str__call_sign(name, args, kwargs, **options))

    return


#-----------------------------------------------------------


def debug_print__call_sign__name(
    name: ty__name,
    should_print: bool = DEFAULT__SHOULD_PRINT,
    **options,
):

    if should_print:
        print(debug_str__call_sign__name(name, **options))

    return


#-----------------------------------------------------------


def debug_print__call_sign__args(
    args: ty.Optional[ty__args] = None,
    kwargs: ty.Optional[ty__kwargs] = None,
    should_print: bool = DEFAULT__SHOULD_PRINT,
    **options,
):

    if should_print:
        print(debug_str__call_sign__args(args, kwargs, **options))

    return


#-----------------------------------------------------------


def debug_print__args(
    args: ty.Optional[ty__args] = None,
    should_print: bool = DEFAULT__SHOULD_PRINT,
    **options,
):

    if should_print:
        print(debug_str__args(args, **options))

    return


#-----------------------------------------------------------


def debug_print__kwargs(
    kwargs: ty.Optional[ty__kwargs] = None,
    should_print: bool = DEFAULT__SHOULD_PRINT,
    **options,
):

    if should_print:
        print(debug_str__kwargs(kwargs, **options))

    return


#-----------------------------------------------------------


def debug_print__messages(
    messages: ty.Optional[ty__messages] = None,
    should_print: bool = DEFAULT__SHOULD_PRINT,
    **options,
):

    if should_print:
        print(debug_str__messages(messages, **options))

    return
