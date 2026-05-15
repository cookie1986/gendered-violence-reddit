import psycopg
from src.db.connect_to_db import get_db_connection

conn = get_db_connection()

def get_post_ids(conn: psycopg.Connection) -> list[tuple]:
    """Retrieve post IDs from the posts table."""
    query = """
        SELECT reddit_id
        FROM posts;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return [row[0] for row in rows]