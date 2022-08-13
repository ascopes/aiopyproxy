# -*- coding: utf-8 -*-
"""Proxy server runner implementation."""

from __future__ import annotations

import asyncio
import logging
from types import TracebackType
from typing import Final, Sequence, Type

import uvloop

logger: Final[logging.Logger] = logging.getLogger(__name__)


class Runner:
    """Proxy server runner implementation."""

    def __init__(self, *, use_uvloop: bool = True) -> None:
        """Initialize the runner.

        Optional parameters
        -------------------
        use_uvloop : bool
            Defaults to `True`. If `False`, then `asyncio.new_event_loop` is
            called to acquire a new event loop rather than
            `uvloop.new_event_loop`. This results in a slower `asyncio`
            experience, but may be easier to debug internally.
        """
        if use_uvloop:
            logger.debug("Using libuv event loop implementation")
            self._loop = uvloop.new_event_loop()
        else:
            logger.debug("Using asyncio event loop implementation")
            self._loop = asyncio.new_event_loop()

    def run_once(self) -> None:
        """Run the proxy and wait until it shuts down."""
        self._loop.run_until_complete(self._run())

    def close(self) -> None:
        """Shut down the runner safely."""
        self._loop.stop()
        self._loop.close()

    async def _run(self) -> None:
        logger.info("Hello, World!")

    def __enter__(self) -> Runner:
        """Return the current runner."""
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        """Shut down the runner safely."""
        self.close()


__all__: Final[Sequence[str]] = ("Runner",)
