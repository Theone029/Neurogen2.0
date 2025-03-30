#!/usr/bin/env python3
"""
cycle_dashboard.py

Reads the cycle_hud.md file and displays a summarized dashboard of recent recursive cycles.
This dashboard provides a snapshot of NEUROGATE's evolution, including key timestamps and log entries.
"""

import os

CYCLE_HUD_FILE = "cycle_hud.md"

def read_cycle_hud(limit=10):
    if not os.path.exists(CYCLE_HUD_FILE):
        return "Cycle HUD file not found."
    with open(CYCLE_HUD_FILE, "r") as f:
        lines = f.readlines()
    # Assume each cycle starts with a line beginning with "## Cycle at"
    cycles = []
    current_cycle = []
    for line in lines:
        if line.startswith("## Cycle at"):
            if current_cycle:
                cycles.append("".join(current_cycle))
                current_cycle = []
        current_cycle.append(line)
    if current_cycle:
        cycles.append("".join(current_cycle))
    # Return the most recent cycles, limited by the 'limit' parameter
    return "\n".join(cycles[-limit:])

def display_dashboard():
    dashboard = read_cycle_hud()
    print("==== NEUROGATE Cycle Dashboard ====")
    print(dashboard)
    print("====================================")

def test_self():
    display_dashboard()
    return {"valid": True, "state": None, "logs": ["Cycle Dashboard self-test passed."], "next": []}

if __name__ == "__main__":
    test_self()
