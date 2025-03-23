import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3

"""
digest_cron.py

Generates a daily memory digest from MongoDB and stores it with a date-stamped tag.
"""

import datetime
from memory_store import MemoryStore

def generate_digest(memories):
    # Summarize memory entries by joining key content and tags
    if not memories:
        return "No memories recorded today."
    summary = "\n".join([f"- {m['content'][:80]}... (tags: {m['tags']})" for m in memories])
    return f"## Daily Digest ({len(memories)} entries)\n\n{summary}"

def store_digest(summary, store):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    store.collection.insert_one({
        "content": summary,
        "tags": ["digest", f"log-{today}"],
        "version": 1,
        "created_at": datetime.datetime.utcnow(),
        "source": "digest_cron"
    })
    print(f"✅ Digest stored under tag 'log-{today}'")

def run_daily_digest():
    store = MemoryStore(collection_name="memories")
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    start = datetime.datetime.strptime(today, "%Y-%m-%d")
    end = start + datetime.timedelta(days=1)

    memories_today = list(store.collection.find({
        "created_at": {"$gte": start, "$lt": end}
    }))

    summary = generate_digest(memories_today)
    store_digest(summary, store)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("\n--- Running Self-Test for DigestCron ---\n")
        # Insert test memory
        test_store = MemoryStore(collection_name="memories")
        test_store.store_memory(
            "NEUROGEN achieved full memory injection efficiency today.",
            tags=["test", "digest"]
        )
        run_daily_digest()
        print("\n--- DigestCron Self-Test Completed ---\n")
