#!/bin/bash
echo "[TEST] Recursive Testbench:"
python3 -m neurogen.recursive_testbench || exit 1

echo "[TEST] Integrity Linter:"
python3 neurogen/integrity_linter.py || exit 1

echo "[✅] ALL TESTS PASSED"
