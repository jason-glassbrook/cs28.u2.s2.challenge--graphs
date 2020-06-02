############################################################

import typing as ty
from dataclasses import dataclass, field

############################################################
#   Arg
############################################################

ty__Name = ty.NewType(
    "Arg_Name",
    str,
)
ty__Cast = ty.NewType(
    "Arg_Cast",
    ty.Callable[[ty.Any], ty.Any],
)
ty__Keywords = ty.NewType(
    "Arg_Keywords",
    ty.Iterable[ty__Name],
)
ty__Value = ty.NewType(
    "Arg_Value",
    ty.Any,
)

############################################################


@dataclass(frozen=True)
class Arg:
    """
    A data class for handling argument information, parsing, and simple validation.
    """

    name: ty__Name
    cast: ty.Optional[ty__Cast] = lambda x: x
    is_keyword: ty.Optional[bool] = False
    keywords: ty.Optional[ty__Keywords] = None
    is_optional: ty.Optional[bool] = False
    default: ty.Optional[ty__Value] = None

    @property
    def is_required(self) -> bool:
        return (not self.is_optional)

    def __post_init__(self):
        """
        Enforce the consistency of the `Arg`'s attributes:

        -   When `keywords` is not empty,
            then `is_keyword` must be `True`.

        -   When `is_keyword` is `True` and `keywords` is `None` or empty,
            then `keywords` must contain `name`.

        -   When `is_keyword` is `False`,
            then `is_optional` must be `False` and `keywords` must be `None`.
        """

        if self.keywords:
            self.is_keyword = True

        if self.is_keyword and not self.keywords:
            self.keywords = (self.name,)

        if not self.is_keyword:
            self.is_optional = False
            self.keywords = None

        return

    def __call__(self, x_in: ty__Value) -> ty__Value:
        """
        A convenient alias for chaining `(Arg).parse` and `(Arg).validate`.
        """

        x_out = self.parse(x_in)
        self.validate(x_out)

        return x_out

    def parse(self, x_in: ty__Value) -> ty__Value:
        """
        Parse the value. If not None, try casting it. Else, use the default.
        Returns the parsed value.
        """

        x_out = self.default

        if x_in is not None:
            try:
                x_out = self.cast(x_in)
            except Exception as error:
                raise Exception("CastError") from error

        return x_out

    def is_valid(self, x: ty__Value) -> bool:
        """
        Test if the value is valid.
        Returns a `bool`.

        WARNING: NOT IMPLEMENTED.
        """

        x_is_valid = True

        return x_is_valid

    def validate(self, x: ty__Value):
        """
        Test if the value is valid and raises `ValidationError` if not.
        Returns nothing.

        WARNING: NOT IMPLEMENTED.
        """

        x_is_valid = self.is_valid(x)

        if not x_is_valid:
            raise Exception("ValidationError", {self.name: x})

        return


############################################################
#   ArgParser
############################################################

ty__ArgIterable = ty.NewType(
    "ArgParser_ArgIterable",
    ty.Iterable[Arg],
)
ty__NameToArgMapping = ty.NewType(
    "ArgParser_NameToArgMapping",
    ty.Mapping[ty__Name, Arg],
)
ty__NameToValueMapping = ty.NewType(
    "ArgParser_NameToValueMapping",
    ty.Mapping[ty__Name, ty__Value],
)
ty__NameToIsValidMapping = ty.NewType(
    "ArgParser_NameToIsValidMapping",
    ty.Mapping[ty__Name, bool],
)

############################################################


@dataclass(frozen=True)
class ArgParser:
    """
    A data class for handling the information, parsing, and simple validation
    of argument lists.
    """

    arg_list: ty__ArgIterable
    ordered_arg_list: ty__ArgIterable = field(init=False)
    keyword_arg_dict: ty__NameToArgMapping = field(init=False)

    def __post_init__(self):
        """
        Process `arg_list` into `ordered_arg_list` and `keyword_arg_dict`.
        """

        self.ordered_arg_list = [arg for arg in self.arg_list if arg.is_keyword is False]

        self.keyword_arg_dict = {
            arg.name: arg
            for arg in self.arg_list
            if arg.is_keyword is True
        }

        return

    def __call__(self, *args, **kwargs) -> ty__NameToValueMapping:
        """
        A convenient alias for chaining `(ArgParser).parse` and `(ArgParser).validate`.
        """

        arg_dict = self.parse(*args, **kwargs)
        self.validate(arg_dict)

        return arg_dict

    def parse(self, *args, **kwargs) -> ty__NameToValueMapping:
        """
        Parse the positional arguments `args` and keyword arguments `kwargs`.
        Returns the parsed values.

        WARNING: NOT IMPLEMENTED.
        """

        arg_dict = {arg.name: None for arg in self.arg_list}

        # iterage through input args, parsing with ordered args
        ordered_count = 0
        for (i, x) in enumerate(args):
            arg = self.ordered_arg_list[i]
            arg_dict[arg.name] = arg.parse(x)
            ordered_count += 1

        # if there are leftover input args, parse using keyword args
        for (i, x) in enumerate(args[(ordered_count + 1):]):
            pass

        for (key, arg) in self.keyword_arg_dict.items():
            arg_dict[key] = arg(kwargs[key])

        return arg_dict

    def is_valid(self, arg_dict: ty__NameToValueMapping) -> ty__NameToIsValidMapping:
        """
        Test if the argument dictionary is valid.
        Returns a mapping of argument names to `bool`s.
        """

        arg_is_valid_dict = {
            arg.name:
            (arg.is_valid(arg_dict[arg.name]) if arg.name in arg_dict else None)
            for arg in self.arg_list
        }

        return arg_is_valid_dict

    def validate(self, arg_dict: ty__NameToValueMapping):
        """
        Test if the values in `arg_dict` are valid and raises `ValidationError` if not.
        Returns nothing.

        WARNING: NOT IMPLEMENTED.
        """

        return
