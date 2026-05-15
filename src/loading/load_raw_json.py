import json
from pathlib import Path
from typing import Iterator, Dict, Any, Union

import psycopg
from psycopg.types.json import Jsonb

from src.db.connect_to_db import get_db_connection

def iter_jsonl(filepath: Union[str, Path]) -> Iterator[Dict[str, Any]]:
    """Yield one dictionary per line from a JSONL file."""
    filepath = Path(filepath)

    with filepath.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def get_reddit_id(record: dict[str, Any], record_type: str) -> str:
    """Get the Reddit item ID from a raw post or comment record."""
    if record_type == "post":
        return record["post_id"]

    if record_type == "comment":
        return record["comment_id"]

    raise ValueError(f"Unknown record_type: {record_type}")


def insert_record(conn: psycopg.Connection, record: Dict[str, Any], record_type: str) -> None:
    """Insert a single JSON record into the database."""
    query = """
        INSERT INTO raw_reddit_items (
            reddit_id,
            kind,
            raw_json
        )
        VALUES (
            %(reddit_id)s,
            %(kind)s,
            %(raw_json)s
        )
        ON CONFLICT (reddit_id, kind) DO NOTHING;
    """
    
    raw_data = {
        "reddit_id": get_reddit_id(record, record_type),
        "kind": record_type,
        "raw_json": Jsonb(record),
    }
    conn.execute(query, raw_data)


def load_jsonl_to_db(filepath: Union[str, Path], record_type: str) -> None:
    """Raw data ingestion. Load PRAW extracted JSONL into the PostgreSQL database."""
    with get_db_connection() as conn:
        for record in iter_jsonl(filepath):
           insert_record(conn, record, record_type)