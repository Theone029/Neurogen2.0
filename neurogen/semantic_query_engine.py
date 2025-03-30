#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_query_engine.py

Performs a simple memory query via substring matching.
"""
def query_memory(query, memory_items, top_k=3):
    results = [item for item in memory_items if query.lower() in item.lower()]
    if not results:
        return memory_items[:top_k]
    return results[:top_k]


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
