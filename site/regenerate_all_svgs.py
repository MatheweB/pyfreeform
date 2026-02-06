#!/usr/bin/env python3
"""
Master SVG Regeneration Script for PyFreeform Wiki

This script finds and runs all SVG generator scripts across the wiki.
Each generator creates visual examples for its corresponding markdown file.

Usage:
    python regenerate_all_svgs.py              # Regenerate all SVGs
    python regenerate_all_svgs.py --section getting-started  # Regenerate one section
    python regenerate_all_svgs.py --verbose    # Show detailed output
"""

from pathlib import Path
import importlib.util
import sys
import argparse
from typing import List


WIKI_ROOT = Path(__file__).parent
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'yellow': '\033[93m',
    'red': '\033[91m',
}


def colorize(text: str, color: str) -> str:
    """Add color to terminal output"""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


def find_all_generators(section: str = None) -> List[Path]:
    """
    Find all *_gen.py files in _svg_generators folders

    Args:
        section: Optional section name to filter (e.g., 'getting-started', 'fundamentals')

    Returns:
        List of generator file paths
    """
    if section:
        patterns = [f"{section}/_svg_generators/*_gen.py",
                    f"{section}/_svg_generators/**/*_gen.py"]
    else:
        patterns = ["**/_svg_generators/*_gen.py",
                    "**/_svg_generators/**/*_gen.py"]

    generators = set()
    for pattern in patterns:
        generators.update(WIKI_ROOT.glob(pattern))
    return sorted(generators)


def run_generator(gen_file: Path, verbose: bool = False) -> bool:
    """
    Import and run a generator file's generate_all() function

    Args:
        gen_file: Path to the generator script
        verbose: Whether to print detailed output

    Returns:
        True if successful, False if error occurred
    """
    try:
        # Import the generator module
        module_name = gen_file.stem
        spec = importlib.util.spec_from_file_location(module_name, gen_file)
        module = importlib.util.module_from_spec(spec)

        # Suppress print statements unless verbose
        if not verbose:
            import io
            import contextlib

            with contextlib.redirect_stdout(io.StringIO()):
                spec.loader.exec_module(module)
        else:
            spec.loader.exec_module(module)

        # Run the generate_all function if available
        if hasattr(module, 'generate_all'):
            if verbose:
                print(f"\n  Running: {gen_file.name}")
            module.generate_all()
            return True
        else:
            # Fall back to running as a subprocess (for __main__-style generators)
            import subprocess
            result = subprocess.run(
                [sys.executable, str(gen_file)],
                capture_output=not verbose,
                text=True
            )
            if result.returncode == 0:
                return True
            else:
                if verbose and result.stderr:
                    print(result.stderr)
                return False

    except Exception as e:
        print(colorize(f"  ✗ ERROR in {gen_file.name}: {e}", 'red'))
        if verbose:
            import traceback
            traceback.print_exc()
        return False


def print_header():
    """Print a nice header"""
    print()
    print(colorize("╔════════════════════════════════════════════════════════════╗", 'blue'))
    print(colorize("║        PyFreeform Wiki - SVG Generator System             ║", 'blue'))
    print(colorize("╚════════════════════════════════════════════════════════════╝", 'blue'))
    print()


def print_summary(total: int, succeeded: int, failed: int):
    """Print summary statistics"""
    print()
    print("=" * 60)
    print(colorize(f"  Total generators: {total}", 'bold'))
    print(colorize(f"  ✓ Succeeded: {succeeded}", 'green'))
    if failed > 0:
        print(colorize(f"  ✗ Failed: {failed}", 'red'))
    print("=" * 60)

    if failed == 0:
        print(colorize("  ✨ All SVG images regenerated successfully!", 'green'))
    else:
        print(colorize(f"  ⚠ {failed} generator(s) had errors", 'yellow'))
    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Regenerate SVG images for PyFreeform wiki documentation'
    )
    parser.add_argument(
        '--section',
        type=str,
        help='Only regenerate SVGs for a specific section (e.g., getting-started, fundamentals)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output from generators'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available generators without running them'
    )

    args = parser.parse_args()

    print_header()

    # Find generators
    generators = find_all_generators(section=args.section)

    if not generators:
        if args.section:
            print(colorize(f"No generators found for section: {args.section}", 'yellow'))
        else:
            print(colorize("No generators found in wiki!", 'yellow'))
        return 1

    # List mode
    if args.list:
        print(f"Found {len(generators)} generator(s):\n")
        for gen_file in generators:
            section = gen_file.parent.parent.name
            print(f"  • {colorize(section, 'blue')}/{gen_file.name}")
        print()
        return 0

    # Generate mode
    if args.section:
        print(f"Regenerating SVGs for section: {colorize(args.section, 'bold')}")
    else:
        print(f"Regenerating {colorize('ALL', 'bold')} SVG images across the wiki")

    print(f"Found {colorize(str(len(generators)), 'bold')} generator script(s)\n")

    succeeded = 0
    failed = 0

    for gen_file in generators:
        section = gen_file.parent.parent.name
        display_name = f"{section}/{gen_file.stem}"

        print(f"  {colorize('→', 'blue')} {display_name}...", end='')
        sys.stdout.flush()

        if run_generator(gen_file, verbose=args.verbose):
            print(colorize(" ✓", 'green'))
            succeeded += 1
        else:
            print(colorize(" ✗", 'red'))
            failed += 1

    print_summary(len(generators), succeeded, failed)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
