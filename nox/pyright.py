# -*- coding: utf-8 -*-
"""Static typechecking using pyright."""
import nox_poetry

pyright_version = "pyright >= 1.1.266, < 1.2"

targets = ["aiopyproxy"]


@nox_poetry.session(reuse_venv=True)
def pyright(session):
    """Run the static type checker."""
    session.poetry.installroot()
    session.install(pyright_version)
    session.run("pyright", *targets)
