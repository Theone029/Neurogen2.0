#!/usr/bin/env python3
"""
memory_store.py

A MongoDB-backed memory storage module for NEUROGEN.
Supports dual-mode invocation: as an imported module or via CLI (for scheduled tasks or Discord triggers).

Usage:
    python3 memory_store.py test    # Run self-test stub
"""

import sys
import os
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

class MemoryStore:
    def __init__(self, mongo_uri=None, db_name="neurogen", collection_name="memory"):
        """
        Initialize the MemoryStore.
        Args:
            mongo_uri (str): MongoDB connection URI.
            db_name (str): Name of the database.
            collection_name (str): Name of the collection.
        """
        if mongo_uri is None:
            mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def store_memory(self, content, tags=None, extra_fields=None):
        """
        Stores a memory entry.
        Args:
            content (str): The memory content.
            tags (list): List of tags for filtering.
            extra_fields (dict): Any additional fields.
        Returns:
            inserted_id: The ID of the stored memory.
        """
        if tags is None:
            tags = []
        if extra_fields is None:
            extra_fields = {}
        memory_doc = {
            "content": content,
            "tags": tags,
            "created_at": datetime.datetime.utcnow(),
        }
        memory_doc.update(extra_fields)
        result = self.collection.insert_one(memory_doc)
        return result.inserted_id

    def get_memory(self, memory_id):
        """
        Retrieves a memory entry by its ID.
        Args:
            memory_id (str or ObjectId): The ID of the memory entry.
        Returns:
            dict: The memory document or None if not found.
        """
        if not isinstance(memory_id, ObjectId):
            try:
                memory_id = ObjectId(memory_id)
            except Exception as e:
                print(f"Invalid memory_id format: {e}")
                return None
        memory_doc = self.collection.find_one({"_id": memory_id})
        return memory_doc

    def query_memories_by_tag(self, tag):
        """
        Retrieves memory entries that include a specific tag.
        Args:
            tag (str): The tag to filter memories.
        Returns:
            list: A list of memory documents.
        """
        cursor = self.collection.find({"tags": tag})
        return list(cursor)

    def update_memory(self, memory_id, new_content=None, add_tags=None, remove_tags=None, extra_fields=None):
        """
        Updates a memory entry.
        Args:
            memory_id (str or ObjectId): The ID of the memory entry.
            new_content (str): New content to update.
            add_tags (list): Tags to add.
            remove_tags (list): Tags to remove.
            extra_fields (dict): Additional fields to update.
        Returns:
            The result of the update operation.
        """
        if not isinstance(memory_id, ObjectId):
            try:
                memory_id = ObjectId(memory_id)
            except Exception as e:
                print(f"Invalid memory_id format: {e}")
                return None
        
        update_ops = {}
        set_ops = {}
        
        if new_content is not None:
            set_ops["content"] = new_content
        if extra_fields:
            set_ops.update(extra_fields)
        if set_ops:
            update_ops["$set"] = set_ops
        if add_tags:
            update_ops["$addToSet"] = {"tags": {"$each": add_tags}}
        if remove_tags:
            update_ops["$pullAll"] = {"tags": remove_tags}

        if not update_ops:
            print("No update operations provided.")
            return None

        result = self.collection.update_one({"_id": memory_id}, update_ops)
        return result

    def delete_memory(self, memory_id):
        """
        Deletes a memory entry by its ID.
        Args:
            memory_id (str or ObjectId): The ID of the memory entry.
        Returns:
            int: The count of deleted documents.
        """
        if not isinstance(memory_id, ObjectId):
            try:
                memory_id = ObjectId(memory_id)
            except Exception as e:
                print(f"Invalid memory_id format: {e}")
                return 0
        result = self.collection.delete_one({"_id": memory_id})
        return result.deleted_count

    def get_daily_digest(self, date=None):
        """
        Retrieves all memory entries created on a specific day.
        Args:
            date (datetime.date): The day for which to retrieve memories. Defaults to today.
        Returns:
            list: A list of memory documents.
        """
        if date is None:
            date = datetime.datetime.utcnow().date()
        start = datetime.datetime.combine(date, datetime.time.min)
        end = datetime.datetime.combine(date, datetime.time.max)
        cursor = self.collection.find({"created_at": {"$gte": start, "$lte": end}})
        return list(cursor)

# Self-Test Stub
def test_memory_store():
    print("\n--- Running Self-Test for MemoryStore ---\n")
    
    # Use a separate database/collection for testing to avoid clashing with production data
    store = MemoryStore(db_name="test_neurogen", collection_name="test_memory")
    
    # Clear the test collection before starting
    store.collection.delete_many({})
    print("Test collection cleared.")

    # 1. Test: Store a memory
    print("\n[TEST] Storing memory...")
    memory_id = store.store_memory("Test memory content", tags=["test", "init"])
    print(f"Memory stored with ID: {memory_id}")

    # 2. Test: Retrieve memory by ID
    print("\n[TEST] Retrieving memory...")
    retrieved = store.get_memory(memory_id)
    print("Retrieved memory:", retrieved)

    # 3. Test: Update memory (modify content & add a tag)
    print("\n[TEST] Updating memory...")
    update_result = store.update_memory(memory_id, new_content="Updated test memory content", add_tags=["updated"])
    if update_result:
        print(f"Update matched: {update_result.matched_count}, modified: {update_result.modified_count}")
    updated = store.get_memory(memory_id)
    print("Updated memory:", updated)

    # 4. Test: Query memories by tag
    print("\n[TEST] Querying memories with tag 'test'...")
    memories_with_test = store.query_memories_by_tag("test")
    print(f"Found {len(memories_with_test)} memory(ies) with tag 'test'.")
    
    # 5. Test: Get daily digest
    print("\n[TEST] Retrieving daily digest...")
    digest = store.get_daily_digest()
    print(f"Daily digest count: {len(digest)}")
    
    # 6. Test: Delete memory
    print("\n[TEST] Deleting memory...")
    delete_count = store.delete_memory(memory_id)
    print(f"Deleted memory count: {delete_count}")
    
    # Final cleanup of test collection
    store.collection.delete_many({})
    print("\nSelf-Test completed.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_memory_store()
    else:
        print("MemoryStore module loaded. To run the self-test, execute:\n  python3 memory_store.py test")
