"""Simplified Chinese entry point for the Specify CLI."""

from __future__ import annotations

import importlib
import os


def main() -> None:
    """Force zh_CN locale before importing the regular CLI runner."""
    os.environ["SPECIFY_LANG"] = "zh_CN"
    module = importlib.import_module("specify_cli")
    module.main()
