#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
# Bootstrap: add the root directory so modules in the root are importable.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_synthesizer import MemorySynthesizer
from distill import distill_text

class ContextInjector:
    def __init__(self):
        self.synthesizer = MemorySynthesizer()

    def inject_context(self, query: str, limit: int = 5) -> str:
        memories = self.synthesizer.synthesize_context(query, limit=limit)
        if not memories:
            return "No relevant memory found."
        combined = ""
        for mem in memories:
            content = mem.get("content", "")
            distilled = distill_text(content, max_length=200)
            combined += distilled + "\n"
        return combined.strip()

def test_context_injector():
    print("\n--- Running Self-Test for Context Injector ---\n")
    injector = ContextInjector()
    query = "recursive intelligence and optimization"
    prompt = injector.inject_context(query)
    print("Injected Prompt:")
    print(prompt)
    print("\n--- Context Injector Self-Test Completed ---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_context_injector()
    else:
        print("Context Injector module loaded.")
