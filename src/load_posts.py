import json
import os
from pathlib import Path
from typing import Iterator, Dict, Any, Union

import psycopg
from dotenv import load_dotenv

load_dotenv()

def iter_jsonl(filepath: Union[str, Path]) -> Iterator[Dict[str, Any]]:
    """Yield one dictionary per line from a JSONL file."""
    filepath = Path(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)
    
def get_db_connection() -> psycopg.Connection:
    """Establish a local connection to the PostgreSQL database."""
    return psycopg.connect(
        host = os.getenv("POSTGRES_HOST", "localhost"),
        port = os.getenv("POSTGRES_PORT", "5432"),
        dbname = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")   
    )

def insert_post(conn: psycopg.Connection, post_data: Dict[str, Any]) -> None:
    """Insert a single Reddit post into the database."""
    query = """
        INSERT INTO posts (
            post_id, 
            subreddit, 
            title, 
            score, 
            author, 
            created_utc, 
            selftext, 
            num_comments, 
            permalink, 
            link
        )
        VALUES (
            %(post_id)s,
            %(subreddit)s,
            %(title)s,
            %(score)s,
            %(author)s,
            to_timestamp(%(created_utc)s),
            %(selftext)s,
            %(num_comments)s,
            %(permalink)s,
            %(link)s
        )
        ON CONFLICT (post_id) DO NOTHING;
    """
    conn.execute(query, post_data)

def load_posts_to_db(filepath: Union[str, Path]) -> None:
    """Load Reddit posts from a JSONL file into the PostgreSQL database."""
    inserted = 0

    with get_db_connection() as conn:
        for post in iter_jsonl(filepath):
           insert_post(conn, post)
           inserted += 1
    print(f"Inserted {inserted} posts into the database.")