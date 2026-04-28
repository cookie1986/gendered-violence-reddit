import pandas as pd
from src.client import get_reddit, get_candidate_posts

def extract_reddit_posts(subreddits: list[str], n: int):
    # Init Reddit
    reddit = get_reddit()

    # Request candidate posts
    posts = [
        get_candidate_posts(
            reddit=reddit,
            subreddit_name=name,
            n = n)
            for name in subreddits
            ]
    return posts