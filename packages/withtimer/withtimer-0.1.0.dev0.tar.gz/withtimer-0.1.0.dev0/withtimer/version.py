from __future__ import absolute_import
from . import (
    __version__,
    __title__,
    __summary__
)


class WithtimerAbout:
    """
    If you need to print the version of WithTimer for some reason,
    instantiate one of these and str() it.

    print(WithTimerAbout())
    """
    def __str__(self):
        return "%s %s version %s" % (__title__, __summary__, __version__)
