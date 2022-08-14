# -*- coding: utf-8 -*-
"""Base server class to extend web server functionality from."""

from __future__ import annotations

import abc
import asyncio
import logging
from typing import Final, Sequence

from aiohttp import web


class Server(abc.ABC):
    """Base class for a basic HTTP server."""

    __slots__: Sequence[str] = (
        "_host",
        "_logger",
        "_loop",
        "_port",
        "_runner",
        "_server",
        "_stopping",
    )

    _host: Final[str]
    _logger: Final[logging.Logger]
    _loop: Final[asyncio.AbstractEventLoop]
    _port: Final[int]
    _runner: Final[web.ServerRunner]
    _server: Final[web.Server]
    _stopping: Final[asyncio.Event]

    def __init__(
        self,
        *,
        handle_signals: bool = True,
        host: str,
        logger: logging.Logger,
        loop: asyncio.AbstractEventLoop,
        port: int,
    ) -> None:
        """Initialize the server.

        Parameters
        ----------
        host : str
            The host to expose the server on. Set to "0.0.0.0" to expose on all
            interfaces, or "localhost" to only expose on loopback interfaces.
        port : int
            The port to expose the server on.
        loop : asyncio.AbstractEventLoop
            The event loop to run on.
        logger : logging.Logger
            The logger to write out logs to.

        Optional Parameters
        -------------------
        handle_signals : bool
            Defaulting to `True`, if `False`, then all signals from the OS will
            be ignored rather than handled.
        """
        self._host = host
        self._logger = logger
        self._loop = loop
        self._port = port
        self._server = web.Server(
            handler=self.handle_request,
            request_factory=None,
            loop=loop,
            access_log=self._logger.getChild("access"),
        )
        self._stopping = asyncio.Event()
        self._runner = web.ServerRunner(
            self._server,
            handle_signals=handle_signals,
        )

    async def start(self) -> None:
        """Start the server on the event loop, and then return."""
        self._stopping.clear()

        self._logger.info("Initializing new server...")
        await self._runner.setup()
        site = web.TCPSite(
            runner=self._runner,
            host=self._host,
            port=self._port,
            reuse_address=True,
            reuse_port=True,
        )
        await site.start()
        self._logger.info("Server is now serving on %s:%s", self._host, self._port)

    async def wait(self) -> None:
        """Wait for the server to terminate."""
        await self._stopping.wait()

    async def stop(self) -> None:
        """Request that the server stops at the next opportunity."""
        self._logger.info(
            "Received a request to shut down server %s:%s", self._host, self._port
        )
        self._stopping.set()

    async def close(self) -> None:
        """Immediately close any resources."""
        self._logger.info("Terminating server on %s:%s", self._host, self._port)
        self._stopping.set()

        # I would have expected to call runner.shutdown() instead, but
        # that implementation appears to be a no-op, so we have to do this
        # instead first. Still call shutdown on the runner afterwards in
        # case the implementation changes in the future.
        await self._server.shutdown()
        await self._runner.shutdown()

    @abc.abstractmethod
    async def handle_request(self, req: web.BaseRequest) -> web.StreamResponse:
        """Handle the given request and return the response.

        Parameters
        ----------
        req : aiohttp.web.BaseRequest
            The incoming HTTP request.

        Returns
        -------
        aiohttp.web.StreamResponse
            Some form of HTTP response.
        """


__all__: Final[Sequence[str]] = ("Server",)
