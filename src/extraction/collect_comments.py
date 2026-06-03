import time

from src.extraction.client import get_reddit
from config import NUM_COMMENTS

def fetch_comments(
        post_id: str,
        sleep_seconds: float = 0.65
        ) -> list[dict]:
    """Fetch the top comments for a given reddit post."""
    reddit = get_reddit()
    submission = reddit.submission(id=post_id)
    time.sleep(sleep_seconds)
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