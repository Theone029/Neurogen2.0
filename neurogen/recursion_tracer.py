#!/usr/bin/env python3
"""
recursion_tracer.py

Logs and visualizes the recursive chain execution of NEUROGEN.
Each recursive cycle’s chain is appended to a log file for audit and analysis.
"""

import logging
import os
from datetime import datetime

# Define the log file for recursion traces.
LOG_PATH = "recursion_trace.log"

# Configure logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RecursionTracer")

def log_recursion(chain):
    """
    Log the provided recursion chain (a list of module names) with a timestamp.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"{timestamp} - Recursion Chain: {chain}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    logger.info("Logged recursion chain: %s", chain)

def test_self():
    """
    Self-test for recursion tracer.
    Logs a dummy recursion chain and returns a success result.
    """
    dummy_chain = ["feedback_core", "mutation_engine", "belief_integrity_net", "contradiction_resolver", "knowledge_graph_engine", "semantic_query_engine", "recursive_context_synth", "meta_prioritization_kernel", "memory_digest", "symbolic_reasoning"]
    log_recursion(dummy_chain)
    return {"valid": True, "state": None, "logs": ["Recursion tracer self-test passed."], "next": []}

if __name__ == "__main__":
    test_self()
