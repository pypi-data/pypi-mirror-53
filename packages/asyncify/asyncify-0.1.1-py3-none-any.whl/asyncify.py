# -*- coding: utf-8 -*-
"""Asyncify your code

...or else...
"""
from asyncio import coroutine
from asyncio import get_event_loop
from functools import partial
from functools import wraps
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def asyncify(funk: F) -> F:
    """

    :param funk:
    :return:
    """

    @coroutine
    @wraps(funk)
    def afunk(*args, loop=None, executor=None, **kwargs):
        """

        :param args:
        :param loop:
        :param executor:
        :param kwargs:
        :return:
        """
        loop = loop if loop else get_event_loop() 
        pfunc = partial(funk, *args, **kwargs)
        return loop.run_in_executor(executor, pfunc)

    return cast(F, afunk)

a = asyncify
async = asyncify

