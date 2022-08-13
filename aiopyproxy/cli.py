# -*- coding: utf-8 -*-
"""Definitions for the command line runner."""
from __future__ import annotations

from typing import Final, Sequence

import click
import colorlog

from aiopyproxy import _meta as meta
from aiopyproxy import runner

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


@main.command("run")
@click.option(
    "--disable-uvloop",
    is_flag=True,
    flag_value=True,
    help="If provided, use the standard asyncio event loop rather than libuv.",
)
def run(
    *,
    disable_uvloop: bool,
) -> None:
    """Run a new proxy server."""
    with runner.Runner(use_uvloop=not disable_uvloop) as new_runner:
        new_runner.run_once()


__all__: Final[Sequence[str]] = ("main",)
