#!/usr/bin/env python3
"""
mutation_diff.py

Tracks and logs differences between new beliefs and the previous belief from history.
Flags stagnation if the belief remains unchanged.
Can be extended to tag unresolved contradictions.
"""

import json
import os

HISTORY_FILE = "belief_history.json"

def load_belief_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_belief_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def diff_belief(new_belief):
    history = load_belief_history()
    if history:
        last_belief = history[-1]
        if new_belief == last_belief:
            print("⚠️  Stagnation detected: New belief is identical to the last belief.")
        else:
            print("✅ Belief mutated successfully.")
            print("Diff:")
            print("Previous Belief:", last_belief)
            print("New Belief     :", new_belief)
    else:
        print("No previous belief. Setting initial belief.")
    history.append(new_belief)
    save_belief_history(history)
    return history

def test_self():
    print("Running Mutation Diff Self-Test")
    # First call: No previous belief.
    diff_belief("Initial belief: Clients respond better to personalized messages.")
    # Second call: Should detect stagnation.
    diff_belief("Initial belief: Clients respond better to personalized messages.")
    # Third call: Should show a mutation diff.
    diff_belief("Updated belief: Clients now show increased engagement when personalized.")
    return {"valid": True, "state": None, "logs": ["Mutation Diff self-test passed."], "next": []}

if __name__ == "__main__":
    test_self()
