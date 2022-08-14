# -*- coding: utf-8 -*-
"""Event loop configuration."""

from __future__ import annotations

import asyncio
import logging
from typing import Final, Iterable, Sequence

logger: Final[logging.Logger] = logging.getLogger(__name__)


def new_event_loop(*, use_uvloop: bool = True) -> asyncio.AbstractEventLoop:
    """Create a new event loop.

    Optional parameters
    -------------------
    use_uvloop : bool
        If `True`, then use libuv to make an event loop. Otherwise,
        use asyncio's native implementation.

    Returns
    -------
    asyncio.AbstractEventLoop
        The new event loop.
    """
    return _new_libuv_event_loop() if use_uvloop else _new_asyncio_event_loop()


def _new_libuv_event_loop() -> asyncio.AbstractEventLoop:
    logger.debug("Initializing new libuv asyncio event loop")

    import uvloop

    return uvloop.new_event_loop()


def _new_asyncio_event_loop() -> asyncio.AbstractEventLoop:
    logger.debug("Initializing new native asyncio event loop")

    return asyncio.new_event_loop()


def tidy_up_and_close(loop: asyncio.AbstractEventLoop) -> None:
    """Cancel any tasks, tidy up resources, and close the event loop."""
    logger.info("Shutting down event loop")

    async def _tidy_up(tasks: Iterable[asyncio.Task]) -> None:
        logger.debug("Shutting down remaining tasks")
        for task in tasks:
            task.cancel("Event loop is closing")
        if tasks:
            await asyncio.wait(tasks)

        logger.debug("Shutting down async generators")
        await loop.shutdown_asyncgens()

        logger.debug("Stopping event loop")
        loop.stop()

    loop.create_task(
        _tidy_up(asyncio.all_tasks(loop)),
        name="Shut down all tasks and async generators",
    )
    loop.run_forever()

    logger.debug("Closing event loop")
    loop.close()


__all__: Final[Sequence[str]] = ("new_event_loop",)
