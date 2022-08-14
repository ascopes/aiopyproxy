# -*- coding: utf-8 -*-
"""Definitions for the command line runner."""
from __future__ import annotations

from typing import Final, Sequence

import click
import colorlog

from aiopyproxy import _meta as meta
from aiopyproxy import forwarding, loop

_logging_levels: Final[Sequence[str]] = (
    "OFF",
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
)


@click.group("aiopyproxy")
@click.option(
    "--logging-level",
    default="INFO",
    type=click.Choice(_logging_levels),
    help="Set the logging level to use. Defaults to 'INFO' if unspecified.",
)
@click.help_option()
@click.version_option(meta.version)
def main(logging_level: str) -> None:
    """A simple HTTP proxy for Python."""  # noqa: D401
    colorlog.basicConfig(level=logging_level)


@main.command("forward")
@click.option(
    "--disable-uvloop",
    is_flag=True,
    flag_value=True,
    help="If provided, use the standard asyncio event loop rather than libuv.",
)
@click.option(
    "--host",
    type=click.STRING,
    default="127.0.0.1",
    help="The host interface to serve on.",
)
@click.option(
    "--port",
    type=click.IntRange(min=1, max=2**16),
    default=8080,
    help="The port to host the proxy on.",
)
def forwarding_proxy(
    *,
    disable_uvloop: bool,
    host: str,
    port: int,
) -> None:
    """Run a new proxy server."""
    event_loop = loop.new_event_loop(use_uvloop=not disable_uvloop)

    proxy = forwarding.ForwardingProxy(
        host=host,
        loop=event_loop,
        port=port,
    )

    try:
        event_loop.run_until_complete(proxy.start())
        event_loop.run_until_complete(proxy.wait())
    finally:
        event_loop.run_until_complete(proxy.close())
        loop.tidy_up_and_close(event_loop)


__all__: Final[Sequence[str]] = ("main",)
