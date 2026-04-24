import json
from config import NUM_POSTS
from src.queries import extract_reddit_data

with open('data/subreddits.json', 'r') as f:
    subreddits = json.load(f)
subreddits = subreddits['subreddits']

extract_reddit_data(subreddits = subreddits, n = NUM_POSTS)