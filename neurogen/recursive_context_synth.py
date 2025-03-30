#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recursive_context_synth.py

Synthesizes a context string from memory items.
"""
def build_context(query, memory_items, max_tokens=50):
    return " | ".join(memory_items)


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
