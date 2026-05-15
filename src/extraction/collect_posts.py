import os
import time
from pathlib import Path
from typing import List

import praw

from src.extraction.client import get_reddit
from utils.save_jsonl import save_posts
from utils.serialisers import reddit_post_to_dict

def fetch_posts(
    reddit: praw.Reddit,
    subreddit_name: str,
    n: int,
    sleep_every: int = 100,
    sleep_seconds: float = 2.0
    ) -> List[praw.models.Submission]:
    """Fetch posts from a subreddit."""
    print(f"Processing subreddit: {subreddit_name}")

    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for i, post in enumerate(subreddit.hot(limit=n), start=1):
        posts.append(post)

        if i % sleep_every == 0:
            time.sleep(sleep_seconds)

    print(f"Fetched {len(posts)} posts from {subreddit_name}")
    return posts


def serialise_posts(posts: List[praw.models.Submission]) -> list[dict]:
    """Convert PRAW Submission objects into serialisable dictionaries."""
    return [reddit_post_to_dict(post) for post in posts]


def save_subreddit_posts_jsonl(
    posts_dict: list[dict],
    subreddit_name: str,
    n: int,
) -> Path:
    """Save serialised subreddit posts to JSONL."""
    raw_posts_dir = Path(os.getenv("RAW_POSTS_DIR", "data/raw/posts/"))
    raw_posts_dir.mkdir(parents=True, exist_ok=True)

    filepath = raw_posts_dir / f"{subreddit_name}_hot_{n}.jsonl"

    save_posts(posts_dict, filepath)

    print(f"Saved {len(posts_dict)} posts to {filepath}")
    return filepath


# Orchestration function
def extract_reddit_posts(subreddits: list[str], n: int) -> list[Path]:
    """Extract posts from multiple subreddits and save them as JSONL."""
    reddit = get_reddit()

    output_files = []

    for subreddit_name in subreddits:
        posts = fetch_posts(
            reddit=reddit,
            subreddit_name=subreddit_name,
            n=n,
        )

        posts_dict = serialise_posts(posts)

        filepath = save_subreddit_posts_jsonl(
            posts_dict=posts_dict,
            subreddit_name=subreddit_name,
            n=n,
        )

        output_files.append(filepath)

    return output_files