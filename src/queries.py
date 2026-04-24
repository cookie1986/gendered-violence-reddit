import pandas as pd
from src.client import get_reddit, get_top_n_posts

def extract_reddit_data(subreddits: list[str], n: int):
    reddit = get_reddit()

    posts = [
        get_top_n_posts(
            reddit=reddit,
            subreddit_name=name,
            n = n)
            for name in subreddits
            ]
    return posts