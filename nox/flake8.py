# -*- coding: utf-8 -*-
"""Flake8 linting."""

import nox_poetry

flake8_version = "flake8 >= 5.0.4, < 6.0"
flake8_plugins = [
    # Disallow explicit line breaks
    "flake8-broken-line ~= 0.5",
    # Disallow builtin shadowing,
    "flake8-builtins ~= 1.5",
    # Ensure magic comments at the start of each file.
    "flake8-coding ~= 1.3",
    # Lint list comprehensions.
    "flake8-comprehensions ~= 3.10",
    # Disallow deprecated API usage.
    "flake8-deprecated ~= 1.3",
    # Lint docstrings.
    "flake8-docstrings ~= 1.6",
    # Lint shebangs.
    "flake8-executable ~= 2.1",
    # Lint functions.
    "flake8-functions ~= 0.0",
    # Disallow mutable function parameter default values.
    "flake8-mutable ~= 1.2",
    # Lint f-strings.
    "flake8-pep3101 ~= 1.3",
    # Warn about the use of the "print" builtin in code.
    "flake8-print ~= 5.0",
    # Disallow Python 2 %s-style strings.
    "flake8-printf-formatting ~= 1.1",
    # Inject pyproject.toml support into flake8.
    "flake8-pyproject ~= 1.1",
    # Lint pytest tests.
    "flake8-pytest ~= 1.4",
    # Lint the use of 'raise'.
    "flake8-raise ~= 0.0",
    # Lint the use of return values.
    "flake8-return ~= 0.1",
    # Enforce string formatting uses f-strings.
    "flake8-use-fstring ~= 1.4",
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
