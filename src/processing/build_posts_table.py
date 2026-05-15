import psycopg
from typing import Any, Dict
from src.db.connect_to_db import get_db_connection

conn = get_db_connection()

def get_raw_posts(conn: psycopg.Connection) -> list[tuple]:
    """Retrieve raw Reddit post records from the raw table."""
    query = """
        SELECT reddit_id, fetched_at, raw_json
        FROM raw_reddit_items
        WHERE kind = 'post';
    """

    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def insert_post(conn: psycopg.Connection, reddit_id: str, fetched_at, raw_json: Dict[str, Any]) -> None:
    """Insert one structured post record into the posts table."""
    query = """
        INSERT INTO posts (
            reddit_id,
            subreddit_name,
            title_raw,
            selftext_raw,
            author,
            score,
            num_comments,
            created_utc,
            url,
            permalink,
            fetched_at
        )
        VALUES (
            %(reddit_id)s,
            %(subreddit_name)s,
            %(title_raw)s,
            %(selftext_raw)s,
            %(author)s,
            %(score)s,
            %(num_comments)s,
            to_timestamp(%(created_utc)s),
            %(url)s,
            %(permalink)s,
            %(fetched_at)s
        )
        ON CONFLICT (reddit_id) DO UPDATE SET
            subreddit_name = EXCLUDED.subreddit_name,
            title_raw = EXCLUDED.title_raw,
            selftext_raw = EXCLUDED.selftext_raw,
            author = EXCLUDED.author,
            score = EXCLUDED.score,
            num_comments = EXCLUDED.num_comments,
            created_utc = EXCLUDED.created_utc,
            url = EXCLUDED.url,
            permalink = EXCLUDED.permalink,
            fetched_at = EXCLUDED.fetched_at;
    """

    post_data = {
        "reddit_id": reddit_id,
        "subreddit_name": raw_json.get("subreddit"),
        "title_raw": raw_json.get("title"),
        "selftext_raw": raw_json.get("selftext"),
        "author": raw_json.get("author"),
        "score": raw_json.get("score"),
        "num_comments": raw_json.get("num_comments"),
        "created_utc": raw_json.get("created_utc"),
        "url": raw_json.get("link"),
        "permalink": raw_json.get("permalink"),
        "fetched_at": fetched_at,
    }

    conn.execute(query, post_data)


def build_posts_table() -> None:
    """Build the structured posts table from raw_reddit_items."""
    with get_db_connection() as conn:
        raw_posts = get_raw_posts(conn)

        for reddit_id, fetched_at, raw_json in raw_posts:
            insert_post(conn, reddit_id, fetched_at, raw_json)

    print(f"Processed {len(raw_posts)} raw posts into posts table.")