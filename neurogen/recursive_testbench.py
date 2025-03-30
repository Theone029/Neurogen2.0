#!/usr/bin/env python3
"""
recursive_testbench.py

Calls .test_self() on all recursive NEUROGEN modules to validate integrity.
"""

import importlib, logging, sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RecursiveTestbench")

MODULES = [
    "feedback_core",
    "mutation_engine",
    "belief_integrity_net",
    "contradiction_resolver",
    "knowledge_graph_engine",
    "semantic_query_engine",
    "recursive_context_synth",
    "meta_prioritization_kernel",
    "memory_digest",
    "symbolic_reasoning"
]

def run_all_tests():
    failed = []
    for name in MODULES:
        try:
            mod = importlib.import_module(f"neurogen.{name}")
            if hasattr(mod, "test_self"):
                logger.info(f"Testing: {name}")
                result = mod.test_self()
                if not isinstance(result, dict) or not result.get("valid", False):
                    failed.append(name)
            else:
                logger.warning(f"{name} has no test_self()")
                failed.append(name)
        except Exception as e:
            logger.error(f"{name} crashed: {e}")
            failed.append(name)

    if failed:
        logger.error("FAILED MODULES: " + ", ".join(failed))
        sys.exit(1)
    else:
        logger.info("ALL MODULES PASSED RECURSIVE TESTS")
        sys.exit(0)

if __name__ == "__main__":
    run_all_tests()
