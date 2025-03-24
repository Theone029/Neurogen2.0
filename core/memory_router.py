#!/usr/bin/env python3
"""
memory_router.py

A module to route memory-related requests intelligently.
Depending on the action, it routes to:
- MemoryStore for storing new memory entries.
- MemorySynthesizer for retrieving context.
- Context Pipeline for building a complete context.

This acts as NEUROGEN's memory traffic controller.
"""

import sys, os
# Bootstrap: add the root directory so modules in the root are importable.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
from core.memory_store import MemoryStore
from memory_synthesizer import MemorySynthesizer
from context_pipeline import build_context

class MemoryRouter:
    def __init__(self, db_name="neurogen", collection_name="memories"):
        self.store = MemoryStore(db_name=db_name, collection_name=collection_name)
        self.synthesizer = MemorySynthesizer(db_name=db_name, collection_name=collection_name)
    
    def route(self, action: str, query: str = "", content: str = "", tags: list = None, **kwargs):
        """
        Routes memory-related requests based on the action.
        
        Parameters:
            action (str): "store", "context", or "build".
            query (str): Used for retrieving context if action is "context" or "build".
            content (str): Used for storing new memory if action is "store".
            tags (list): Optional tags for filtering or storing.
            kwargs: Additional parameters (e.g., source for store, limit for context retrieval).
        
        Returns:
            For "store": the inserted memory ID.
            For "context": a list of memory entries.
            For "build": a combined context string.
        """
        if action == "store":
            # Store new memory.
            return self.store.store_memory(content, tags=tags, **kwargs)
        elif action == "context":
            # Retrieve context using the synthesizer.
            return self.synthesizer.synthesize_context(query, tags=tags, limit=kwargs.get("limit", 5))
        elif action == "build":
            # Build full context using the context pipeline.
            return build_context(query)
        else:
            raise ValueError(f"Action '{action}' is not recognized.")

# --- Self-Test Stub ---
def test_memory_router():
    print("\n--- Running Self-Test for MemoryRouter ---\n")
    router = MemoryRouter()

    # Test 1: Store a new memory.
    memory_id = router.route("store", content="Test memory from router: always improve recursive loops.", tags=["router", "test"], source="manual")
    print(f"[TEST] Stored memory ID: {memory_id}")

    # Test 2: Retrieve context via synthesizer.
    context = router.route("context", query="recursive loops", tags=["router", "test"], limit=5)
    print(f"[TEST] Retrieved context ({len(context)} entries):")
    for mem in context:
        print(f"- {mem.get('content', '')[:60]}... (tags: {mem.get('tags')})")

    # Test 3: Build full context via the pipeline.
    full_context = router.route("build", query="recursive loops")
    print("\n[TEST] Built full context:")
    print(full_context)

    print("\n--- MemoryRouter Self-Test Completed ---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_memory_router()
    else:
        print("MemoryRouter module loaded. To run the self-test, execute:\n  python3 core/memory_router.py test")
