import praw
from src.extraction.client import get_reddit

def test_reddit_connection():
    reddit = get_reddit()
    # Basic type check
    assert isinstance(reddit, praw.Reddit)
    # Trigger API call
    user = reddit.user.me()
    assert user is None or isinstance(user, str)


def test_can_read_subreddit():
    reddit = get_reddit()
    subreddit = reddit.subreddit("news")
    post = next(subreddit.hot(limit=1))
    # Confirm a non-empty string
    assert post.title