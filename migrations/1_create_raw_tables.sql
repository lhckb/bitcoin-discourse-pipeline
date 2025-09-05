CREATE TABLE IF NOT EXISTS POSTS_RAW (
    post_id TEXT PRIMARY KEY,
    origin TEXT,
    query_start_time DOUBLE PRECISION,
    post_created_utc DOUBLE PRECISION,
    post_title TEXT,
    -- TODO WIP
)