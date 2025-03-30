#!/bin/bash
cd "$(dirname "$0")"
PYTHONPATH=. python3 -m neurogen.core_loop_test
