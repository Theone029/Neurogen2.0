# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import sys, os
# Bootstrap: add the root directory to Python path for proper module imports.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_synthesizer import MemorySynthesizer
from distill import distill_text

def build_context(query: str, limit: int = 5) -> str:
    """
    Build context for a query by retrieving and distilling memory entries.
    Returns a single string containing the distilled context.
    """
    synthesizer = MemorySynthesizer()
    memories = synthesizer.synthesize_context(query, limit=limit)
    if not memories:
        return "No relevant memory found."
    combined = ""
    for mem in memories:
        content = mem.get("content", "")
        # Distill each memory's content for brevity.
        distilled = distill_text(content, max_length=200)
        combined += distilled + "\n"
    return combined.strip()

# --- Self-Test Stub ---
def test_context_pipeline():
    print("\n--- Running Self-Test for Context Pipeline ---\n")
    query = "recursive intelligence"
    context = build_context(query)
    print("Context built:")
    print(context)
    print("\n--- Context Pipeline Self-Test Completed ---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_context_pipeline()
    else:
        print(build_context("recursive intelligence"))
