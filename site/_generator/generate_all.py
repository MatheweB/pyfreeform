#!/usr/bin/env python3
"""Regenerate all SVGs for wiki_v2.

Usage:
    python -m wiki_v2._generator.generate_all          # Run all
    python -m wiki_v2._generator.generate_all guide     # Run only guide generators
    python -m wiki_v2._generator.generate_all --list    # List discovered generators
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

GENERATORS_DIR = Path(__file__).parent


def discover_generators(filter_section: str | None = None) -> list[Path]:
    """Find all gen_*.py files, optionally filtered by section."""
    generators = sorted(GENERATORS_DIR.rglob("gen_*.py"))
    if filter_section:
        generators = [g for g in generators if filter_section in str(g)]
    return generators


def module_name_for(gen_path: Path) -> str:
    """Convert a generator file path to a Python module name."""
    # Get path relative to wiki_v2's parent
    wiki_v2_root = GENERATORS_DIR.parent
    project_root = wiki_v2_root.parent
    rel = gen_path.relative_to(project_root)
    return str(rel).replace("/", ".").replace("\\", ".").removesuffix(".py")


def run_generator(gen_path: Path) -> tuple[bool, str]:
    """Run a single generator. Returns (success, message)."""
    module_path = module_name_for(gen_path)
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "generate"):
            module.generate()
            return True, "OK"
        else:
            return False, "No generate() function found"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def run_all(filter_section: str | None = None) -> bool:
    """Run all generators, report results."""
    generators = discover_generators(filter_section)

    if not generators:
        section_msg = f" matching '{filter_section}'" if filter_section else ""
        print(f"No generators found{section_msg}")
        return True

    print(f"Found {len(generators)} generator(s)\n")

    passed, failed = 0, 0
    start_total = time.time()

    for gen_path in generators:
        name = f"{gen_path.parent.name}/{gen_path.name}"
        start = time.time()
        success, message = run_generator(gen_path)
        elapsed = time.time() - start

        if success:
            passed += 1
            print(f"  OK   {name}  ({elapsed:.1f}s)")
        else:
            failed += 1
            print(f"  FAIL {name}: {message}")

    total_time = time.time() - start_total
    print(f"\n{passed} passed, {failed} failed out of {len(generators)} ({total_time:.1f}s)")
    return failed == 0


def main():
    args = sys.argv[1:]

    if "--list" in args:
        for g in discover_generators():
            print(f"  {g.parent.name}/{g.name}")
        return

    filter_section = args[0] if args else None
    success = run_all(filter_section)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
