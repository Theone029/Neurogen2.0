import sys
import os
import datetime

# Add the root directory to Python path so that modules in the root are importable.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_store import MemoryStore
from auto_tag import generate_tags

class MemorySynthesizer:
    def __init__(self, db_name="neurogen", collection_name="memories"):
        self.store = MemoryStore(db_name=db_name, collection_name=collection_name)
        
    def query_memories_by_tags(self, tags: list) -> list:
        # Union all memory entries that have any of the tags (avoid duplicates)
        seen = {}
        results = []
        for tag in tags:
            memories = self.store.query_memories_by_tag(tag)
            for m in memories:
                _id = str(m.get("_id"))
                if _id not in seen:
                    seen[_id] = m
                    results.append(m)
        return results

    def synthesize_context(self, query: str, tags: list = None, limit: int = 5) -> list:
        if not tags:
            tags = generate_tags(query)
        results = self.query_memories_by_tags(tags)
        sorted_results = sorted(results, key=lambda m: m.get("created_at", datetime.datetime.min), reverse=True)
        return sorted_results[:limit]

# --- Test Mode ---
def test_synthesizer():
    print("\n--- Running Self-Test for MemorySynthesizer ---\n")
    synth = MemorySynthesizer()

    query = "Optimize memory injection and reduce GPT token waste."
    print(f"[TEST] Query: {query}")
    context = synth.synthesize_context(query)
    print(f"Context Retrieved ({len(context)} entries):")
    for mem in context:
        print(f"- {mem.get('content', '')[:60]}... (tags: {mem.get('tags')})")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_synthesizer()
