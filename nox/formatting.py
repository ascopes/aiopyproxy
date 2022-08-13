# -*- coding: utf-8 -*-
"""Pipelines for enforcing code style."""
import nox_poetry

dependencies = [
    "black >= 22.3, < 23",
    "isort >= 5.10, < 6",
]
paths = ["aiopyproxy", "nox", "noxfile.py"]


@nox_poetry.session(reuse_venv=True)
def check_formatting(session):
    """Ensure code formatting guidelines are met."""
    session.install(*dependencies)
    session.run("black", "--check", *paths)
    session.run("isort", "--check", *paths)


@nox_poetry.session(reuse_venv=True)
def reformat(session):
    """Reformat code."""
    session.install(*dependencies)
    session.run("black", *paths)
    session.run("isort", *paths)
