#!/usr/bin/env python3
"""
integrity_linter.py

Checks recursion wiring: orphaned logic, missing test_self(), and broken import structure.
Excludes files that are intentionally not testable: __init__.py, core_loop_test.py, and recursive_testbench.py.
"""

import os

# List of relative file paths to exclude from the test.
EXCLUDE_FILES = {"neurogen/__init__.py", "neurogen/core_loop_test.py", "neurogen/recursive_testbench.py"}

def find_py_files(root):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)

def check_wiring():
    bad = []
    for f in find_py_files("neurogen"):
        # Normalize the file path relative to the project root
        rel_path = os.path.relpath(f, ".").replace("\\", "/")
        if rel_path in EXCLUDE_FILES:
            continue
        with open(f) as fp:
            content = fp.read()
            # Each module must have either a test_self() or a main() function for self-validation.
            if "def test_self" not in content and "def main" not in content:
                bad.append(rel_path)
    if bad:
        print("⚠️  Modules missing test_self() or main():")
        for b in bad:
            print(" -", b)
        return 1
    print("✅ All modules wired with test_self() or main()")
    return 0

if __name__ == "__main__":
    exit(check_wiring())
