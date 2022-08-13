# -*- coding: utf-8 -*-
"""Definitions for the command line runner."""
from typing import Final, Sequence

import click
import colorlog

from ._meta import version

_logging_levels: Final[Sequence[str]] = [
    "OFF",
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
]


@click.group("aiopyproxy")
@click.option(
    "--logging-level",
    default="INFO",
    type=click.Choice(_logging_levels),
    help="Set the logging level to use. Defaults to 'INFO' if unspecified.",
)
@click.help_option()
@click.version_option(version)
def main(logging_level: str) -> None:
    """A simple HTTP proxy for Python."""  # noqa: D401
    colorlog.basicConfig(level=logging_level)
