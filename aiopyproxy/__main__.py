# -*- coding: utf-8 -*-
"""Entrypoint for the module from the commandline."""
from __future__ import annotations

from typing import Final, Sequence

from aiopyproxy import cli

cli.main()

__all__: Final[Sequence[str]] = ()
