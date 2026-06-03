import psycopg
from src.db.connect_to_db import get_db_connection

def query_all_posts() -> list[tuple]:
    """Get posts from the posts table."""
    
    conn = get_db_connection()
    
    query = """
        SELECT reddit_id AS reddit_post_id, 
        subreddit_name, 
        title_raw, 
        selftext_raw, 
        author AS post_author, 
        score AS post_score, 
        created_utc, 
        url AS post_url
        FROM posts;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return rows

def query_all_comments() -> list[tuple]:
    """Get comments from the comments table."""
    
    conn = get_db_connection()
    
    query = """
        SELECT reddit_id AS reddit_comment_id, 
        post_id, 
        author AS comment_author, 
        body_raw, 
        score AS comment_score, 
        created_utc
        FROM comments;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return rows
