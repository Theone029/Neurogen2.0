#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feedback_core.py

Processes agent output and flags if mutation is required.
"""
def process_feedback(agent_name, outcome):
    mutation_required = False
    # If the outcome is negative, set mutation_required to True.
    if "poor" in outcome.lower() or "low" in outcome.lower():
        mutation_required = True
    # Always return valid, but include the mutation flag.
    return {"valid": True, "mutation_required": mutation_required}


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
