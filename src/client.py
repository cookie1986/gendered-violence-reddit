import praw
import os
import time
from typing import List
from dotenv import load_dotenv
from utils.save_jsonl import save_posts
from utils.serialisers import reddit_sub_to_dict

load_dotenv()

# Module level cache
_reddit_instance = None

def get_reddit() -> praw.Reddit:
    """Create and return an authenticated reddit instance"""
    
    global _reddit_instance
    
    if _reddit_instance is None:
        _reddit_instance = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent = os.getenv("USER_AGENT"),
            ratelimit_seconds=300
        )
    return _reddit_instance


def get_candidate_posts(
        reddit: praw.Reddit, 
        subreddit_name: str, 
        n: int,
        sleep_every: int = 100,
        sleep_seconds: float = 2.0
        ) -> List[praw.models.Submission]:
    
    print(f"Processing Subreddit: {subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    
    posts = []

    for i, post in enumerate(subreddit.hot(limit=n), start=1):
        posts.append(post)
        # Safeguard against hitting API limits (note: reddit already handles this)
        if i % sleep_every == 0:
            time.sleep(sleep_seconds)
    
    # Convert submission to dict
    posts_dict = [reddit_sub_to_dict(post) for post in posts]
            
    # Store the dict output
    filename = f"{os.getenv('RAW_POSTS_DIR')}{subreddit_name}_hot_{n}.jsonl"
    save_posts(posts_dict, filename)
    print(f"{subreddit_name} processed")

    return posts
