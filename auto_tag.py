#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_tag.py

A module to automatically tag memory entries based on content analysis.
Uses a simple heuristic approach to generate tags from text.
Extendable to incorporate AI-driven tagging in the future.
"""

import re

class AutoTag:
    def __init__(self, keyword_tags=None):
        self.keyword_tags = keyword_tags or {
            "error": "debugging",
            "debug": "debugging",
            "fix": "debugging",
            "fail": "bug",
            "test": "testing",
            "optimize": "performance",
            "refactor": "maintenance",
            "memory": "data",
            "inject": "logic",
            "success": "achievement",
            "deploy": "deployment",
            "recursive": "recursive",
            "intelligence": "intelligence",
            "context": "context",
            "evolution": "evolution",
            "architecture": "architecture"
        }

    def generate(self, text: str) -> list:
        tags = set()
        for word in text.lower().split():
            for k, v in self.keyword_tags.items():
                if k in word:
                    if isinstance(v, list):
                        tags.update(v)
                    else:
                        tags.add(v)
        return list(tags or {"misc"})

def generate_tags(text: str) -> list:
    return AutoTag().generate(text)

def test_auto_tag():
    print("\n--- Running Self-Test for AutoTag ---")
    tests = [
        "We encountered an error during deployment. Debug the code.",
        "Successful test run leads to a successful deploy!",
        "Time to refactor and optimize the memory synthesizer.",
        "No issues here, just pure success.",
        "Recursive intelligence in context is key for evolution."
    ]
    for i, test in enumerate(tests, 1):
        print(f"\n[TEST {i}] Input: {test}")
        tags = generate_tags(test)
        print(f"Generated Tags: {tags}")
    print("\n--- AutoTag Self-Test Completed ---")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_auto_tag()
