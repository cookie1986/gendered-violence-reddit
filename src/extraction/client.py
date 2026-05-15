import praw
import os
from dotenv import load_dotenv

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