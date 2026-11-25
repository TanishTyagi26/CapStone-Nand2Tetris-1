
"""
compare.py - Hack Machine Code (.hack) Comparison Tool

Compares student assembler output with official Nand2Tetris .hack files.

Usage:
    python compare.py
    python compare.py Add
    python compare.py my.hack official.hack
"""

import sys
import os
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SEARCH_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "tests"),
    os.path.join(BASE_DIR, "capstone"),
    os.path.join(BASE_DIR, "capstone", "tests")
]


def find_file(filename):
    """Search for a file in available project directories."""

    for directory in SEARCH_DIRS:
        path = os.path.join(directory, filename)

        if os.path.isfile(path):
            return path

    return None


def compare_hack_files(actual_path, expected_path, test_name=""):
    """
    Compare two .hack files line by line.
    Returns (is_match, total_lines, diff_list).
    """

    name_str = f" [{test_name}]" if test_name else ""

    print("\n=======================================================")
    print(f"Comparing{name_str}:")
    print(f"  Actual   : {actual_path}")
    print(f"  Expected : {expected_path}")
    print("=======================================================")

    if not os.path.exists(actual_path):
        print(f"[FAIL] Output file not found: {actual_path}")
        return False, 0, [f"Missing file: {actual_path}"]

    if not os.path.exists(expected_path):
        print(f"[SKIP] Official comparison file not found: {expected_path}")
        return None, 0, []

    with open(actual_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    with open(expected_path, "r", encoding="utf-8") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    total_actual = len(actual_lines)
    total_expected = len(expected_lines)

    diffs = []
    max_len = max(total_actual, total_expected)

    for i in range(max_len):

        act = actual_lines[i] if i < total_actual else "<MISSING - EOF>"
        exp = expected_lines[i] if i < total_expected else "<EXTRA LINE>"

        if act != exp:
            diffs.append((i + 1, act, exp))

    if not diffs:
        print(f"[PASS] PERFECT MATCH! All {total_expected} instructions match.")
        return True, total_expected, []

    print(
        f"[FAIL] Found {len(diffs)} difference(s) "
        f"(actual={total_actual}, expected={total_expected}):"
    )

    for line_num, act, exp in diffs[:10]:
        print(f"\n  Line {line_num}:")
        print(f"    Your Output    : {act}")
        print(f"    Official Match : {exp}")

    if len(diffs) > 10:
        print(f"\n  ... and {len(diffs) - 10} more differences.")

    return False, total_expected, diffs


def run_all_tests():
    """Run comparisons for Add, Max, Rect, and Pong."""

    targets = ["Add", "Max", "Rect", "Pong"]
    results = {}

    for name in targets:

        actual_path = find_file(f"{name}.hack")

        expected_names = [
            f"{name}_official.hack",
            f"{name}.cmp",
            f"official_{name}.hack",
            os.path.join("official", f"{name}.hack")
        ]

        expected_path = None

        for filename in expected_names:
            expected_path = find_file(filename)

            if expected_path:
                break

        if not actual_path:

            asm_path = find_file(f"{name}.asm")

            if asm_path:
                assembler_path = find_file("assembler.py")

                if not assembler_path:
                    print("\n[ERROR] assembler.py not found.")
                    results[name] = "ASSEMBLER NOT FOUND"
                    continue

                print(f"\n[*] Assembling {asm_path} first...")

                subprocess.run(
                    [
                        sys.executable,
                        assembler_path,
                        os.path.basename(asm_path)
                    ],
                    cwd=os.path.dirname(asm_path),
                    check=False
                )

                actual_path = os.path.splitext(asm_path)[0] + ".hack"

        if actual_path and expected_path:

            matched, total, _ = compare_hack_files(
                actual_path,
                expected_path,
                test_name=name
            )

            results[name] = "PASSED" if matched else "FAILED"

        elif actual_path:

            print(f"\n[{name}] Actual output exists: {actual_path}")
            print(f"Official reference file not found.")
            results[name] = "WAITING FOR OFFICIAL FILE"

        else:

            print(f"\n[{name}] Neither .hack nor .asm file found.")
            results[name] = "NOT FOUND"

    print("\n" + "=" * 55)
    print("              TEST SUMMARY REPORT")
    print("=" * 55)

    for name, status in results.items():
        print(f"  {name:10s} : {status}")

    print("=" * 55 + "\n")


if __name__ == "__main__":

    if len(sys.argv) == 3:

        # Compare any two specified files
        compare_hack_files(sys.argv[1], sys.argv[2])

    elif len(sys.argv) == 2:

        # Compare a program by name
        target = sys.argv[1].replace(".hack", "").replace(".asm", "")

        actual = find_file(f"{target}.hack")
        expected = find_file(f"{target}_official.hack")

        if actual and expected:
            compare_hack_files(actual, expected, test_name=target)
        else:
            print(f"[ERROR] Could not find both files for {target}.")

    else:

        # Run all standard tests
        run_all_tests()
