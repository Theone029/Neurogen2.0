#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mutation_engine.py

Mutates state if feedback indicates poor performance.
"""
def mutate_if_needed(state):
    output = state.get("output", "")
    if "poor" in output.lower():
        # Generate a new belief that contradicts the old, unproductive one.
        return {"mutated": True, "new_belief": "Clients respond better to personalized messages."}
    return {"mutated": False}


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
