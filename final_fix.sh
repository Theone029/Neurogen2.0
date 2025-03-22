#!/bin/bash
set -e

echo "==> Stopping any service using port 8001..."
sudo fuser -k 8001/tcp || true

echo "==> Stopping memory_api service if running..."
sudo systemctl stop memory_api || true

echo "==> Replacing mainmemory.py with final stable version..."
cat > /home/assistant/neurogen/mainmemory.py <<'EOF2'
#!/usr/bin/env python3
import os
import sys
import logging
import traceback
import numpy as np
import openai
from datetime import datetime
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field, constr

import psycopg2
from psycopg2 import OperationalError, IntegrityError
from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool

from prometheus_client import Counter, generate_latest
from slowapi import Limiter
from slowapi.util import get_remote_address

from dotenv import load_dotenv

load_dotenv()
openai.api_key = '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'

API_KEY = os.getenv("API_KEY", "supersecureapikey123")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "memory_bank"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "JackKumo2020*"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

logging.basicConfig(level=logging.INFO)

try:
    pool = SimpleConnectionPool(minconn=1, maxconn=10, **DB_CONFIG)
    logging.info("Database connection pool created successfully.")
except Exception as e:
    logging.error(f"Error creating connection pool: {e}")
    sys.exit(1)

@contextmanager
def db_connection():
    conn = None
    try:
        conn = pool.getconn()
        conn.autocommit = True
        yield conn
    except OperationalError as e:
        logging.error(f"Operational DB error: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable")
    finally:
        if conn:
            pool.putconn(conn)

limiter = Limiter(key_func=get_remote_address)

def verify_api_key(api_key: str = Header(None, alias="API_KEY")):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

request_counter = Counter("api_requests", "Count of API requests")

class MemoryEntry(BaseModel):
    project: constr(max_length=100) = Field(..., description="Project name")
    topic: constr(max_length=100) = Field(..., description="Topic")
    content: constr(max_length=2000) = Field(..., description="Content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")

app = FastAPI(
    title="AI Memory System",
    description="Persistent AI Memory System with Semantic Search, API Security, Automation, and Scalability",
    version="1.0.0"
)

@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    request_counter.inc()
    response = await limiter.limit("10/minute")(call_next)(request)
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

def get_embedding(text):
    try:
        response = openai.embeddings.create(model="text-embedding-ada-002", input=[text])
        return response.data[0].embedding
    except Exception as e:
        logging.error("OpenAI embedding API error: " + str(e))
        raise e

@app.post("/store", response_model=dict, summary="Store memory", dependencies=[Depends(verify_api_key)])
def store_memory(entry: MemoryEntry):
    try:
        embedding = get_embedding(entry.content)
        with db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "INSERT INTO memories (project, topic, content, timestamp, embedding) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (entry.project, entry.topic, entry.content, entry.timestamp, np.array(embedding).tolist())
                )
                new_id = cur.fetchone()[0]
                logging.info(f"Memory stored with ID {new_id}")
                return {"status": "Memory stored successfully", "id": new_id}
    except IntegrityError as e:
        logging.error(f"Integrity DB error: {e}")
        raise HTTPException(status_code=400, detail="Integrity constraint violated")
    except Exception as e:
        logging.error("Unexpected error in store_memory: " + str(e))
        raise HTTPException(status_code=500, detail=str(e) + " :: " + traceback.format_exc())

@app.get("/recall", response_model=dict, summary="Recall memory", dependencies=[Depends(verify_api_key)])
def recall_memory(project: str, topic: str, limit: int = 3, offset: int = 0):
    query = """
    SELECT content, timestamp FROM memories
    WHERE project = %s AND topic = %s
    ORDER BY timestamp DESC
    LIMIT %s OFFSET %s;
    """
    try:
        with db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, (project, topic, limit, offset))
                rows = cur.fetchall()
                if not rows:
                    raise HTTPException(status_code=404, detail="No memories found")
                return {"memories": [{"content": row["content"], "timestamp": row["timestamp"]} for row in rows]}
    except Exception as e:
        logging.error("Unexpected error in recall_memory: " + str(e))
        raise HTTPException(status_code=500, detail=str(e) + " :: " + traceback.format_exc())

@app.get("/semantic_recall", response_model=dict, summary="Semantic recall memory", dependencies=[Depends(verify_api_key)])
def semantic_recall(query: str, project: str, limit: int = 3):
    try:
        q_embedding = get_embedding(query)
        with db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "SELECT content FROM memories ORDER BY embedding <=> %s LIMIT %s;",
                    (np.array(q_embedding).tolist(), limit)
                )
                rows = cur.fetchall()
                return {"memories": [row["content"] for row in rows]}
    except Exception as e:
        logging.error("Unexpected error in semantic_recall: " + str(e))
        raise HTTPException(status_code=500, detail=str(e) + " :: " + traceback.format_exc())

@app.get("/health", response_model=dict, summary="Health check")
def health_check():
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                _ = cur.fetchone()
    except Exception as e:
        logging.error("Health check failed: " + str(e))
        raise HTTPException(status_code=503, detail="Service Unavailable")
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Debug endpoint to show OpenAI API key
@app.get("/debug_test", response_model=dict, summary="Debug Test Endpoint")
def debug_test():
    try:
        return {"openai_api_key": openai.api_key}
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

if __name__ == "__main__":
    try:
        script_path = os.path.abspath(__file__)
        backup_path = script_path + ".bak"
        with open(script_path, "r") as orig:
            code = orig.read()
        with open(backup_path, "w") as bak:
            bak.write(code)
        logging.info(f"Backup saved to {backup_path}")
    except Exception as e:
        logging.error("Backup failed: " + str(e))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
