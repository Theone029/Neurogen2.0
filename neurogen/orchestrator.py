#!/usr/bin/env python3
"""
orchestrator.py

Daemonized orchestrator for NEUROGEN that:
- Executes the core_loop recursively at fixed intervals.
- Logs each cycle's results to cycle_hud.md.
- Triggers git autosync (via autopush.sh) on successful cycles.
"""

import os
import sys
# Ensure the project root is in sys.path so that 'neurogen' can be imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import datetime
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Orchestrator")

try:
    from neurogen.core_loop_test import core_loop
except ImportError as e:
    logger.error("Failed to import core_loop: %s", e)
    exit(1)

# Path to the cycle dashboard log
CYCLE_HUD_PATH = "cycle_hud.md"

def log_cycle(result):
    """Append the cycle output to cycle_hud.md."""
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(CYCLE_HUD_PATH, "a") as f:
        f.write(f"## Cycle at {timestamp}\n")
        for line in result.get("log", []):
            f.write(f"- {line}\n")
        f.write("\n")
    logger.info("Cycle logged to %s", CYCLE_HUD_PATH)

def git_autopush():
    """Call the autopush.sh script to commit and push changes."""
    try:
        subprocess.check_call(["./autopush.sh"])
        logger.info("Git autopush executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error("Git autopush failed: %s", e)

def main_loop():
    # Set the cycle interval (in seconds, e.g., 300 sec = 5 minutes)
    cycle_interval = 300
    logger.info("NEUROGEN Orchestrator started. Cycle interval: %d seconds.", cycle_interval)
    while True:
        logger.info("Starting new recursive cycle...")
        # Prepare system state (replace with real state as needed)
        state = {
            "output": "Engagement was low due to poor personalization.",
            "belief": "All clients should be sent the same message.",
            "query": "How to increase lead response rate?"
        }
        # Run the core recursive loop
        result = core_loop(state)
        # Log the cycle results
        log_cycle(result)
        # If cycle succeeded, trigger git autosync
        if result.get("success", False):
            logger.info("Cycle passed. Triggering git autopush...")
            git_autopush()
        else:
            logger.error("Cycle failed. Skipping git push.")
        logger.info("Cycle complete. Sleeping for %d seconds...", cycle_interval)
        time.sleep(cycle_interval)

if __name__ == "__main__":
    main_loop()
