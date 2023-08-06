import asyncio
import functools

from .wrap_tools import find_subclass, add_method, del_method

__all__ = (
    'run_blocking_io', 'wait', 'run',
    'cancel_all_tasks', 'shutdown_loop',
    'coroutine'
)

coroutine = find_subclass('coroutine')


async def run_blocking_io(func, *args, **kwargs):
    """|coro|

    Run some blocking function in an event loop.

    If there is a running loop, ``'func'`` is executed in it.

    Otherwise, a new loop is being created and closed at the end of the execution.

    Example:

    .. code-block:: python3

        def make_image():
            ...  # long code of creating an image

        # somewhere in an async function:

        await run_blocking_io(make_image)
    """
    loop = asyncio._get_running_loop()

    if loop is None:
        loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))


async def wait(fs, *, loop=None, timeout=None, return_when='ALL_COMPLETED'):
    """A function that is calling :func:`asyncio.wait`.

    Used for less imports inside and outside of this library.

    Wait for the Futures and coroutines given by fs to complete.

    The sequence futures must not be empty.

    Coroutines will be wrapped in Tasks.

    Returns two sets of Future: (done, pending).

    Usage:

    .. code-block:: python3

        done, pending = await gd.utils.wait(fs)

    .. note::

        This does not raise :exc:`TimeoutError`! Futures that aren't done
        when the timeout occurs are returned in the second set.
    """
    try:
        fs = list(fs)
    except TypeError:  # not iterable
        pass
    return await asyncio.wait(fs, loop=loop, timeout=timeout, return_when=return_when)


def run(coro, *, loop=None, debug: bool = False):
    """Run a |coroutine_link|_.

    This function runs the passed coroutine, taking care
    of the event loop and shutting down asynchronous generators.

    This function is basically ported from Python 3.7 for backwards compability
    with earlier versions of Python.

    This function cannot be called when another event loop is
    running in the same thread.

    If ``debug`` is ``True``, the event loop will be run in debug mode.

    This function creates a new event loop and closes it at the end if a ``loop`` is ``None``.

    If a loop is given, this function basically calls :meth:`asyncio.AbstractEventLoop.run_until_complete`.

    It should be used as a main entry point to asyncio programs, and should
    ideally be called only once.

    Example:

    .. code-block:: python3

        async def test(pid):
            return pid

        one = gd.utils.run(test(1))

    Parameters
    ----------
    coro: |coroutine_link|_
        Coroutine to run.

    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        A loop to run ``coro`` with. If ``None`` or omitted, a new event loop is created.

    debug: :class:`bool`
        Whether or not to run event loop in debug mode.

    Returns
    -------
    `Any`
        Anything that ``coro`` returns.
    """

    if asyncio._get_running_loop() is not None:
        raise RuntimeError('Can not perform gd.utils.run() in a running event loop.')

    if not asyncio.iscoroutine(coro):
        raise ValueError('A coroutine was expected, got {!r}.'.format(coro))

    # if a loop is given, let's just run our coro in it
    if loop is not None:
        return loop.run_until_complete(coro)

    loop = asyncio.new_event_loop()

    try:
        asyncio.set_event_loop(loop)
        loop.set_debug(debug)
        return loop.run_until_complete(coro)

    finally:
        shutdown_loop(loop, True)


def cancel_all_tasks(loop, f_name: str = 'gd.utils.run'):
    """Cancels all tasks in a loop.

    Parameters
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        Event loop to cancel tasks in.
    """
    try:
        to_cancel = asyncio.all_tasks(loop)
    except AttributeError:  # py < 3.7
        to_cancel = asyncio.Task.all_tasks(loop)

    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(
        asyncio.gather(*to_cancel, loop=loop, return_exceptions=True)
    )

    for task in to_cancel:
        if task.cancelled():
            continue

        if task.exception() is not None:
            loop.call_exception_handler({
                'message': 'Unhandled exception during {}() shutdown'.format(f_name),
                'exception': task.exception(),
                'task': task
            })


def shutdown_loop(loop, set_event_loop_to_none: bool = False):
    try:
        cancel_all_tasks(loop)
        loop.run_until_complete(loop.shutdown_asyncgens())

    finally:
        if set_event_loop_to_none:
            asyncio.set_event_loop(None)

        loop.close()


def _run(self, loop=None):
    """Run the coroutine in a new event loop,
    closing the loop after execution (if not given).
    """

    if loop is None:
        loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    return loop.run_until_complete(self)


def enable_run_method(on: bool = True):
    """Add or delete 'run' method of a coroutine."""
    if on:
        add_method(coroutine, _run, name='run')
    else:
        del_method(coroutine, 'run')

enable_run_method()
