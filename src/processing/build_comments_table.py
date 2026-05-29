import psycopg
from typing import Dict, Any
from src.db.connect_to_db import get_db_connection
from src.queries.get_post_ids_from_db import get_post_ids
from src.extraction.client import get_reddit
from config import NUM_COMMENTS

def get_comments_for_post(post_id: str) -> list[dict]:
    """Fetch the top comments for a given reddit post."""
    reddit = get_reddit()
    submission = reddit.submission(id=post_id)
    submission.comment_sort = "top"
    submission.comments.replace_more(limit=0)
    top_comments = submission.comments[:NUM_COMMENTS]

    comments_data = []
    for comment in top_comments:
        comments_data.append({
            "reddit_id": comment.id,
            "post_id": post_id,
            "author": str(comment.author),
            "body_raw": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc
        })
    
    return comments_data

def insert_comment(conn: psycopg.Connection, comment_data: Dict[str, Any]) -> None:
    """Insert one strctured comment record into the comments table."""
    query = """
        INSERT INTO comments (
            reddit_id,
            post_id,
            author,
            body_raw,
            score,
            created_utc
        )
        VALUES (
            %(reddit_id)s,
            %(post_id)s,
            %(author)s,
            %(body_raw)s,
            %(score)s,
            to_timestamp(%(created_utc)s)
        )
        ON CONFLICT (reddit_id) DO UPDATE SET
            post_id = EXCLUDED.post_id,
            author = EXCLUDED.author,
            body_raw = EXCLUDED.body_raw,
            score = EXCLUDED.score,
            created_utc = EXCLUDED.created_utc;
        """
    
    conn.execute(query, comment_data)


def build_comments_table() -> None:
    """Build the structured comments table."""
    with get_db_connection() as conn:
        post_ids = get_post_ids(conn)
    
        for post_id in post_ids:
            comments = get_comments_for_post(post_id)

            for comment in comments:
                insert_comment(conn, comment)

    print(f"Processed {len(post_ids)} posts into comments table.")