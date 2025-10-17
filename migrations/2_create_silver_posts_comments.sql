CREATE TABLE IF NOT EXISTS silver_posts (
    post_id TEXT PRIMARY KEY,
    origin TEXT,
    author TEXT,
    query_start_time TIMESTAMP,
    post_title TEXT,
    post_selftext TEXT,
    post_created_utc TIMESTAMP,
    original_title_char_count INTEGER,
    original_selftext_char_count INTEGER,
    post_title_normalized TEXT,
    post_selftext_normalized TEXT,
    normalized_title_char_count INTEGER,
    normalized_selftext_char_count INTEGER
);
-- rollback DROP TABLE IF EXISTS silver_posts;

CREATE TABLE IF NOT EXISTS silver_comments (
    comment_id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    comment_author TEXT,
    comment_body TEXT,
    comment_created_utc TIMESTAMP,
    query_start_time TIMESTAMP,
    original_comment_char_count INTEGER,
    comment_body_normalized TEXT,
    normalized_comment_char_count INTEGER,
    FOREIGN KEY (post_id) REFERENCES silver_posts (post_id)
);
-- rollback DROP TABLE IF EXISTS silver_comments;
