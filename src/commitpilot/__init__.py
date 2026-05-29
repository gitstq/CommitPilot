"""
CommitPilot - Intelligent Git Commit Assistant CLI
智能Git提交助手

A lightweight, zero-dependency CLI tool for intelligent Git commit message generation.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from commitpilot.core import CommitAnalyzer, MessageGenerator
from commitpilot.cli import main

__all__ = ["CommitAnalyzer", "MessageGenerator", "main"]
