import json
from config import NUM_POSTS
from src.queries import extract_reddit_posts
from src.load_posts import load_posts_to_db

# with open('data/subreddits.json', 'r') as f:
#     subreddits = json.load(f)
# subreddits = subreddits['subreddits']

# for subreddit in subreddits:
#     extract_reddit_posts(subreddits = subreddits, n = NUM_POSTS)

load_posts_to_db(filepath = 'data/raw/Feminism_hot_10.jsonl')