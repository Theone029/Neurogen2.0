#!/usr/bin/env python3
"""
auto_tag.py

A module to automatically tag memory entries based on content analysis.
Uses a simple heuristic approach to generate tags from text.
Extendable to incorporate AI-driven tagging in the future.
"""

import re

class AutoTag:
    def __init__(self, keyword_tags=None):
        """
        Initialize AutoTag with an optional mapping of keywords to tags.
        Args:
            keyword_tags (dict): Mapping where keys are keywords (str) and values are tags (str or list of str).
        """
        # Default keyword-to-tag mapping—customize as needed.
        if keyword_tags is None:
            keyword_tags = {
                "error": "bug",
                "fail": "bug",
                "success": "achievement",
                "optimize": "performance",
                "deploy": "deployment",
                "test": "testing",
                "debug": "debugging",
                "refactor": "maintenance",
                "memory": "data",
                "synthesizer": "logic",
            }
        self.keyword_tags = keyword_tags

    def generate_tags(self, text):
        """
        Analyze the text and generate a list of tags.
        Args:
            text (str): The content to analyze.
        Returns:
            list: A list of unique tags found in the text.
        """
        text_lower = text.lower()
        found_tags = set()
        for keyword, tag in self.keyword_tags.items():
            # Use word boundaries to ensure we match whole words
            if re.search(r"\b" + re.escape(keyword) + r"\b", text_lower):
                if isinstance(tag, list):
                    found_tags.update(tag)
                else:
                    found_tags.add(tag)
        return list(found_tags)

# Self-Test Stub
def test_auto_tag():
    print("\n--- Running Self-Test for AutoTag ---\n")
    auto_tagger = AutoTag()
    
    test_inputs = [
        "We encountered an error during deployment. Debug the code.",
        "Successful test run leads to a successful deploy!",
        "Time to refactor and optimize the memory synthesizer.",
        "No issues here, just pure success."
    ]
    
    for idx, text in enumerate(test_inputs, 1):
        tags = auto_tagger.generate_tags(text)
        print(f"[TEST {idx}] Input: {text}")
        print(f"Generated Tags: {tags}\n")

    print("--- AutoTag Self-Test Completed ---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_auto_tag()
    else:
        print("AutoTag module loaded. To run the self-test, execute:\n  python3 auto_tag.py test")
