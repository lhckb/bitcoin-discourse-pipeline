CREATE TABLE IF NOT EXISTS bronze_posts (
    origin              TEXT,          -- source system
    author              TEXT,
    query_start_time    DOUBLE PRECISION,  -- ingestion timestamp
    post_id             TEXT,          -- Reddit post ID (base36)
    post_title          TEXT,          -- post title
    post_selftext       TEXT,          -- post body text
    post_created_utc    DOUBLE PRECISION,  -- post creation time
    post_comments       JSONB          -- raw array of comments (nested JSON)
);
-- DROP TABLE IF EXISTS bronze_posts;