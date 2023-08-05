import asyncio
import traceback
from typing import Any, Awaitable, Generator, List, TypeVar, Union

T = TypeVar('T')

LAST_CANCEL_BY: List[str] = []

CoroArg = Union[Awaitable[T], Generator[Any, None, T]]


class Task(asyncio.Task):

    def cancel(self) -> bool:
        if super().cancel():
            LAST_CANCEL_BY[:] = traceback.format_stack()
            return True
        else:
            return False


def create_task(loop: asyncio.AbstractEventLoop,
                coro: CoroArg[T]) -> asyncio.Task[T]:
    return Task(coro, loop=loop)


def install_task_factory(loop: asyncio.AbstractEventLoop = None) -> None:
    if loop is None:
        loop = asyncio.get_event_loop()
    loop.set_task_factory(create_task)


def last_cancel_by() -> str:
    return '\n'.join(LAST_CANCEL_BY)
