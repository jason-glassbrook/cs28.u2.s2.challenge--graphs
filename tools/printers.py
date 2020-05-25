############################################################
#   PRINTERS
############################################################

import re
import math

############################################################

DEFAULT__WIDTH = 20

DEFAULT__DENT__COUNT = 1
DEFAULT__DENT__DENTER = (" " * 2)

DEFAULT__LINE__LINER = "-"
DEFAULT__LINE__WIDTH = DEFAULT__WIDTH

DEFAULT__HEADING__UPPER = "="
DEFAULT__HEADING__LOWER = "-"
DEFAULT__HEADING__WIDTH = None
DEFAULT__HEADING__WIDTH_STEP = DEFAULT__WIDTH
DEFAULT__HEADING__BETWEEN_MESSAGES = " "

NEWLINE = re.compile(r"[\r\n]+")

#-----------------------------------------------------------


def print_on(*args, **print_kwargs):

    print(*args, **print_kwargs, end="")

    return


def print_dent(
    *args,
    count=DEFAULT__DENT__COUNT,
    denter=DEFAULT__DENT__DENTER,
    **print_kwargs,
):

    dent = (denter * count)

    print_on(dent)
    print(*args, **print_kwargs)

    return


def print_line(
    width=DEFAULT__LINE__WIDTH,
    liner=DEFAULT__LINE__LINER,
    **print_kwargs,
):

    line = (liner * width)[:width]    # user can provide `liner` longer than 1 char

    print(line, **print_kwargs)

    return


def print_heading(
    *messages,
    width=DEFAULT__HEADING__WIDTH,
    width_step=DEFAULT__HEADING__WIDTH_STEP,
    upper=DEFAULT__HEADING__UPPER,
    lower=DEFAULT__HEADING__LOWER,
    between_messages=DEFAULT__HEADING__BETWEEN_MESSAGES,
    **print_kwargs,
):

    # build content
    content = None
    content_width = 0

    if messages:
        content = between_messages.join(messages)
        content_width = max(map(len, NEWLINE.split(content)))

    # if `width` not set, dynamically set it
    if width is None:
        steps = math.ceil(content_width / width_step)
        width = width_step * (steps or 1)

    # print the heading
    if upper is not None:
        print_line(width, liner=upper, **print_kwargs)
    if content is not None:
        print(content, **print_kwargs)
    if lower is not None:
        print_line(width, liner=lower, **print_kwargs)

    return
