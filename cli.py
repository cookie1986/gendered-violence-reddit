import json
import sys

from config import NUM_POSTS
from src.extraction.collect_posts import extract_reddit_posts
from src.loading.load_raw_json import load_jsonl_to_db
from src.processing.build_posts_table import build_posts_table
from src.processing.build_comments_table import build_comments_table


def get_subreddits():
    with open('data/subreddits.json', 'r') as f:
        subreddits = json.load(f)
    return subreddits['subreddits']

def run_reddit_extraction():
    subreddits = get_subreddits()
    extract_reddit_posts(subreddits = subreddits, n = NUM_POSTS)

def run_load_json_to_db():
    subreddits = get_subreddits()
    for subreddit in subreddits:
        filepath = f"data/raw/{subreddit}_hot_{NUM_POSTS}.jsonl"
        load_jsonl_to_db(filepath=filepath, record_type='post')

def run_build_posts_table():
    build_posts_table()

def run_build_comments_table():
    build_comments_table()

def run_all():
    run_reddit_extraction()
    run_load_json_to_db()
    run_build_posts_table()
    run_build_comments_table()


# CLI entry point
if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "all"

    if command == "extract":
        run_reddit_extraction()
    elif command == "load":
        run_load_json_to_db()
    elif command == "build_posts":
        run_build_posts_table()
    elif command == "build_comments":
        run_build_comments_table()
    elif command == "all":
        run_all()
    else:
        print(f"Unknown command: {command}")