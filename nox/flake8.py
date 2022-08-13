# -*- coding: utf-8 -*-
"""Flake8 linting."""

import nox_poetry

flake8_version = "flake8 >= 5.0.4, < 6.0"
flake8_plugins = [
    "flake8-broken-line",
    "flake8-builtins",
    "flake8-coding",
    "flake8-comprehensions",
    "flake8-deprecated",
    "flake8-docstrings",
    "flake8-executable",
    "flake8-fixme",
    "flake8-functions",
    "flake8-mutable",
    "flake8-pep3101",
    "flake8-print",
    "flake8-printf-formatting",
    "flake8-pytest-style",
    "flake8-raise",
    "flake8-use-fstring",
]


targets = [
    "aiopyproxy",
    "noxfile.py",
    "nox",
]


@nox_poetry.session(reuse_venv=True)
def flake8(session):
    """Run flake8 linting."""
    session.poetry.installroot()
    session.install(flake8_version, *flake8_plugins)
    session.run(
        "flake8",
        "--benchmark",
        "--show-source",
        "--tee",
        *targets,
    )
