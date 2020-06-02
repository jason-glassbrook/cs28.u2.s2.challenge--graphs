############################################################
#   NUMBERS
############################################################

import string

############################################################

DEFAULT__ALPHABET = (string.digits + string.ascii_letters + "!?")
DEFAULT__BASE = 10

DEFAULT__INCLUDE_BASE = None    # None or 0, "before" or < 0, "after" or > 0
DEFAULT__INCLUDE_BASE__BETWEEN = "'"    # string between base and number
DEFAULT__INCLUDE_BASE__BEFORE_BASE = ""    # string before base
DEFAULT__INCLUDE_BASE__AFTER_BASE = ""    # string after base

#-----------------------------------------------------------


def int_as_base(
    number,
    base=DEFAULT__BASE,
    alphabet=DEFAULT__ALPHABET,
):

    if base > len(alphabet):
        raise Exception("int_as_base.BaseLargerThanAlphabet")

    result = ""

    while number:

        result += alphabet[number % base]
        number //= base

    return result[::-1] or "0"


#-----------------------------------------------------------


def int_to_str(
    number,
    base=DEFAULT__BASE,
    alphabet=DEFAULT__ALPHABET,
    fill=None,
    width=None,
):

    if fill is None:
        fill = alphabet[0]

    if width is None:
        width = ""

    return "{0:{fill}>{width}}".format(
        int_as_base(number, base=base, alphabet=alphabet),
        fill=fill,
        width=width,
    )
