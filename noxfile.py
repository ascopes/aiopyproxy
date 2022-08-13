# -*- coding: utf-8 -*-
"""Noxfile that loads scripts from the 'nox' directory.

This keeps each script simpler and tidier in the long run.
"""
import os
import runpy

here = os.path.dirname(os.path.abspath(__file__))
nox_dir = os.path.join(here, "nox")

for file in os.listdir(nox_dir):
    file = os.path.join(nox_dir, file)
    if file.endswith(".py"):
        runpy.run_path(file, init_globals=None, run_name=file.removesuffix(".py"))
