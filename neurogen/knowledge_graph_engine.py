#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_graph_engine.py

Builds a symbolic knowledge graph from beliefs.
"""
class KnowledgeGraph:
    def __init__(self):
        self.beliefs = []
    def add_belief(self, belief, context=None, tags=None):
        self.beliefs.append({"belief": belief, "context": context, "tags": tags})
KG = KnowledgeGraph()


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
