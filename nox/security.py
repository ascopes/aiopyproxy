# -*- coding: utf-8 -*-
"""Security checking."""
import nox_poetry

bandit_version = "bandit >= 1.7.4, < 2"
safety_version = "safety >= 2.1.1, < 3"


@nox_poetry.session()
def sast(session):
    """Run static application security testing."""
    session.install(bandit_version)
    session.run("bandit", "-r", "aiopyproxy")


@nox_poetry.session()
def sca(session):
    """Run software composition analysis."""
    session.poetry.installroot()
    session.install(safety_version)
    session.run("safety", "check")
