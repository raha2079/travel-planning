#!/usr/bin/env python3
"""Standalone verifier test script (uses argparse for CLI testing)."""

import argparse as _argparse
import sys as _sys
from pathlib import Path as _Path

# Add parent directory to path
_sys.path.insert(0, str(_Path(__file__).parent.parent))

from verifier.task import verify


def main():
    """Main CLI entry point for testing."""
    parser = _argparse.ArgumentParser(description="Independently validate a travel-planning result and workflow trace")
    parser.add_argument("output", nargs="?", default=str(_Path(__file__).resolve().parent / "output.json"))
    parser.add_argument("--request", default=str(_Path(__file__).resolve().parent / "request.json"))
    parser.add_argument("--options", default=str(_Path(__file__).resolve().parent / "options.json"))
    parser.add_argument("--trace", default=str(_Path(__file__).resolve().parent / "action_trace.json"))
    args = parser.parse_args()

    errors = verify(args.output, args.request, args.options, args.trace)

    if not errors:
        print("PASS")
        return 0
    else:
        print("FAIL")
        for error in errors:
            print(error)
        return 1


if __name__ == "__main__":
    _sys.exit(main())
