#!/usr/bin/env python3
"""
orchestrator.py

Daemonized orchestrator for NEUROGEN that:
- Executes the core_loop recursively at fixed intervals.
- Logs each cycle's results to cycle_hud.md.
- Triggers git autosync (via autopush.sh) on successful cycles.
- Integrates live agent management.
- Injects external signals from the external_signal_bridge into the system state.
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

try:
    from neurogen.agent_manager import AgentManager
except ImportError as e:
    logger.error("Failed to import AgentManager: %s", e)
    exit(1)

try:
    from neurogen.external_signal_bridge import process_external_signals
except ImportError as e:
    logger.error("Failed to import external_signal_bridge: %s", e)
    # If external signals fail, we continue with an empty list.
    def process_external_signals():
        return []

# Path to the cycle dashboard log.
CYCLE_HUD_PATH = "cycle_hud.md"

def log_cycle(result):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(CYCLE_HUD_PATH, "a") as f:
        f.write(f"## Cycle at {timestamp}\n")
        for line in result.get("log", []):
            f.write(f"- {line}\n")
        f.write("\n")
    logger.info("Cycle logged to %s", CYCLE_HUD_PATH)

def git_autopush():
    try:
        subprocess.check_call(["./autopush.sh"])
        logger.info("Git autopush executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error("Git autopush failed: %s", e)

def main_loop():
    # Set the cycle interval (in seconds).
    cycle_interval = 300
    logger.info("NEUROGEN Orchestrator started. Cycle interval: %d seconds.", cycle_interval)
    
    # Initialize Agent Manager and spawn initial agents.
    agent_manager = AgentManager()
    agent_manager.spawn_initial_agents()
    
    while True:
        logger.info("Starting new recursive cycle...")
        # Prepare base system state.
        state = {
            "output": "Engagement was low due to poor personalization.",
            "belief": "All clients should be sent the same message.",
            "query": "How to increase lead response rate?"
        }
        # Fetch external signals and inject into state.
        external_signals = process_external_signals()
        if external_signals:
            state["external_signals"] = external_signals
            logger.info("External signals integrated: %s", external_signals)
        else:
            logger.info("No external signals received this cycle.")
        
        # Run the core recursive loop.
        result = core_loop(state)
        log_cycle(result)
        
        # Run agent management tasks: update and terminate agents.
        agent_manager.monitor_agents()
        agent_manager.terminate_underperformers()
        active_agents = agent_manager.registry.get_active_agents()
        logger.info("Active agents count: %d", len(active_agents))
        
        if result.get("success", False):
            logger.info("Cycle passed. Triggering git autopush...")
            git_autopush()
        else:
            logger.error("Cycle failed. Skipping git push.")
        
        logger.info("Cycle complete. Sleeping for %d seconds...", cycle_interval)
        time.sleep(cycle_interval)

if __name__ == "__main__":
    main_loop()
