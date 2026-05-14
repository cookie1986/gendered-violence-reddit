CREATE TABLE IF NOT EXISTS raw_reddit_items (
    id BIGSERIAL PRIMARY KEY,
    reddit_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    fetched_at TIMESTAMPTZ DEFAULT NOW(),
    raw_json JSONB NOT NULL,
    UNIQUE (reddit_id, kind)
);

CREATE TABLE IF NOT EXISTS posts (
    post_id TEXT PRIMARY KEY,
    subreddit TEXT,
    title TEXT,
    score INTEGER,
    permalink TEXT,
    author TEXT,
    created_utc TIMESTAMPTZ,
    selftext TEXT,
    num_comments INTEGER,
    link TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    post_id TEXT REFERENCES posts(post_id),
    parent_id TEXT,
    subreddit TEXT,
    author TEXT,
    created_utc TIMESTAMPTZ,
    body TEXT,
    score INTEGER,
    processed_text TEXT,
    processing_version TEXT
);

CREATE INDEX IF NOT EXISTS idx_posts_subreddit_created
ON posts (subreddit, created_utc);

CREATE INDEX IF NOT EXISTS idx_comments_post_id
ON comments (post_id);

CREATE INDEX IF NOT EXISTS idx_comments_parent_id
ON comments (parent_id);

CREATE INDEX IF NOT EXISTS idx_raw_reddit_items_raw_json
ON raw_reddit_items USING GIN (raw_json);