CREATE TABLE IF NOT EXISTS raw_reddit_items (
    id BIGSERIAL PRIMARY KEY,
    reddit_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    fetched_at TIMESTAMPTZ DEFAULT NOW(),
    raw_json JSONB NOT NULL,
    UNIQUE (reddit_id, kind)
);

CREATE TABLE IF NOT EXISTS posts (
    id BIGSERIAL PRIMARY KEY,
    reddit_id TEXT NOT NULL UNIQUE,
    subreddit_name TEXT NOT NULL,
    title_raw TEXT,
    selftext_raw TEXT,
    author TEXT,
    score INTEGER,
    num_comments INTEGER,
    created_utc TIMESTAMPTZ,
    url TEXT,
    permalink TEXT,
    fetched_at TIMESTAMPTZ,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS comments (
    id BIGSERIAL PRIMARY KEY,
    reddit_id TEXT NOT NULL UNIQUE,
    post_id TEXT NOT NULL,
    author TEXT,
    body_raw TEXT,
    score INTEGER,
    created_utc TIMESTAMPTZ,
    fetched_at TIMESTAMPTZ DEFAULT NOW(),

    FOREIGN KEY (post_id)
        REFERENCES posts (reddit_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_posts_subreddit_created
ON posts (subreddit_name, created_utc);

CREATE INDEX IF NOT EXISTS idx_comments_post_id
ON comments (post_id);

CREATE INDEX IF NOT EXISTS idx_comments_parent_id
ON comments (post_id);

CREATE INDEX IF NOT EXISTS idx_raw_reddit_items_raw_json
ON raw_reddit_items USING GIN (raw_json);