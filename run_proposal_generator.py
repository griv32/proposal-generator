#!/usr/bin/env python3
"""
Direct runner for Proposal Generator - works without installation.

This script allows users to run the proposal generator directly after cloning,
without needing to install the package.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from proposal_generator.cli import main  # type: ignore[import-untyped]
except ImportError as e:
    print(f"Error importing proposal_generator: {e}")
    print("\nTo use this direct runner, you need to install dependencies first:")
    print("Option 1 (UV - Recommended):")
    print("  uv sync")
    print("  uv run python run_proposal_generator.py --help")
    print("\nOption 2 (pip):")
    print("  pip install -e .")
    print("  python run_proposal_generator.py --help")
    print("\nAlternatively, use UV directly:")
    print("  uv run proposal-generator --help")
    print(f"\nCurrent directory: {Path.cwd()}")
    sys.exit(1)

if __name__ == "__main__":
    main()
