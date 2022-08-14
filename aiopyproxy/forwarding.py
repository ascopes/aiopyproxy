# -*- coding: utf-8 -*-
"""Simple forwarding proxy implementation."""

from __future__ import annotations

import asyncio
import logging
from typing import Final, Sequence

from aiohttp import client, web

from aiopyproxy import server

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ForwardingProxy(server.Server):
    """A simple forwarding HTTP proxy."""

    __slots__: Sequence[str] = ("_client",)

    def __init__(
        self,
        *,
        host: str,
        loop: asyncio.AbstractEventLoop,
        port: int,
    ) -> None:
        """Initialize the forwarding proxy.

        Parameters
        ----------
        host : str
            The host to expose the server on. Set to "0.0.0.0" to expose on all
            interfaces, or "localhost" to only expose on loopback interfaces.
        port : int
            The port to expose the server on.
        loop : asyncio.AbstractEventLoop
            The event loop to run on.
        """
        super().__init__(
            host=host,
            logger=logger,
            loop=loop,
            port=port,
        )
        self._client = client.ClientSession(loop=self._loop)

    async def close(self) -> None:
        """Close the proxy server immediately."""
        try:
            await super().close()
        finally:
            await self._client.close()

    async def handle_request(self, req: web.BaseRequest) -> web.StreamResponse:
        """Proxy the inbound HTTP request to the host in the path."""
        async with self._client.request(
            req.method,
            req.path,
            headers=req.headers,
            allow_redirects=False,
        ) as client_resp:
            server_resp = web.StreamResponse(
                status=client_resp.status,
                reason=client_resp.reason,
                headers=client_resp.headers,
            )

            await server_resp.prepare(req)
            total_bytes = 0

            async for chunk in client_resp.content.iter_any():
                await server_resp.write(chunk)
                total_bytes += len(chunk)

            await server_resp.write_eof()

            return server_resp


__all__: Final[Sequence[str]] = ("ForwardingProxy",)
