from utils.logging_init import setup_logging
import polars as pl
from models.bronze import BronzePostData
import textacy.preprocessing.replace as rep
import textacy.preprocessing.normalize as norm
import textacy.preprocessing.remove as rmv
import emoji
from datetime import datetime, timezone
from common.db import PGSQLConnector

logger = setup_logging()

class RedditSilver:

    def __init__(self, data: list[BronzePostData]):
        dict_data = [d.post_to_dict() for d in data]
        self.posts_df = pl.DataFrame(dict_data)
        self.connector = PGSQLConnector()

    def insert_into_silver_tables(self, posts_df: pl.DataFrame, comments_df: pl.DataFrame):
        p = posts_df["post_id"]
        c = comments_df.filter(
            ~pl.col("post_id").is_in(p)
        )
        if len(c) > 0:
            logger.error("thing")

        self.connector.insert_polars(posts_df, "silver_posts")
        logger.info("Inserted Posts into database")
        self.connector.insert_polars(comments_df, "silver_comments")
        logger.info("Inserted Comments into database")

    def explode_comments(self):
        exploded = self.posts_df.explode("comments")
        self.comments_df = exploded.select([
            pl.col("post_id"),
            pl.col("comments").struct.field("comment_author").alias("comment_author"),
            pl.col("comments").struct.field("comment_id").alias("comment_id"),
            pl.col("comments").struct.field("comment_body").alias("comment_body"),
            pl.col("comments").struct.field("comment_created_utc").alias("comment_created_utc"),
            pl.col("query_start_time")
        ])
        self.posts_df.drop_in_place("comments")
        logger.info("Created separate DF for comments")

    def add_metadata_round_one(self):
        self.posts_df = self.posts_df.with_columns(
            pl.col("post_title").str.len_chars().alias("original_title_char_count"),
            pl.col("post_selftext").str.len_chars().alias("original_selftext_char_count")
        )
        self.comments_df = self.comments_df.with_columns(
            pl.col("comment_body").str.len_chars().alias("original_comment_char_count"),
        )
        logger.info("Added metadata: original text fields char count")
    
    def remove_dupes(self):
        """
        Remove duplicate entries by post_id from the current working df.
        Having post_id as primary key in table definition makes it impossible
        to insert duplicates (if there are already in silver table).

        Drop if text is the exact same in post title, selftext and comment body
        """
        self.posts_df = self.posts_df.unique(subset="post_id")
        self.posts_df = self.posts_df.unique(subset=["post_title", "post_selftext"])
        self.comments_df = self.comments_df.unique(subset="comment_id")
        self.comments_df = self.comments_df.unique(subset="comment_body")
        logger.info("Removed duplicates by filtering equal IDs and text bodies")

    def handle_missing(self):
        """
        Drop if title and selftext are empty
        Drop if comment is empty
        Drop if there are no comments (?)
        """
        self.posts_df = self.posts_df.with_columns([
            pl.col("post_title").cast(pl.Utf8).fill_null(""),
            pl.col("post_selftext").cast(pl.Utf8).fill_null("")
        ])
        self.comments_df = self.comments_df.with_columns([
            pl.col("comment_body").cast(pl.Utf8).fill_null("")
        ])
        # Drop posts where title AND selftext are empty
        self.posts_df = self.posts_df.filter(
            (pl.col("post_title").str.len_chars() > 0) & 
            (pl.col("post_selftext").str.len_chars() > 0)
        )
        # Drop comments that are empty or removed
        self.comments_df = self.comments_df.filter(
            (pl.col("comment_body").str.len_chars() > 0) &
            ~(pl.col("comment_body") == "[removed]")
        )
        logger.info("Filter out rows where all text bodies are empty")

    def normalize_text(self):
        """
        Normalize text to lowercase, remove accentuation, line breaks, urls, emails ...
        """
        self.posts_df = self.posts_df.with_columns(
            pl.col("post_title").map_elements(self.normalize_text_helper, skip_nulls=True, return_dtype=pl.Utf8).alias("post_title_normalized"),
            pl.col("post_selftext").map_elements(self.normalize_text_helper, skip_nulls=True, return_dtype=pl.Utf8).alias("post_selftext_normalized")
        )
        self.comments_df = self.comments_df.with_columns(
            pl.col("comment_body").map_elements(self.normalize_text_helper, skip_nulls=True, return_dtype=pl.Utf8).alias("comment_body_normalized"),
        )
        logger.info("Normalized text using helper function")

    def add_metadata_round_two(self):
        self.posts_df = self.posts_df.with_columns(
            pl.col("post_title_normalized").str.len_chars().alias("normalized_title_char_count"),
            pl.col("post_selftext_normalized").str.len_chars().alias("normalized_selftext_char_count")
        )
        self.comments_df = self.comments_df.with_columns(
            pl.col("comment_body_normalized").str.len_chars().alias("normalized_comment_char_count"),
        )
        logger.info("Added metadata: normalized text char count")

    def convert_unix_to_timestamp(self):
        self.posts_df = self.posts_df.with_columns(
            pl.col("query_start_time").map_elements(self.timestamp_to_datetime_utc),
            pl.col("post_created_utc").map_elements(self.timestamp_to_datetime_utc),
        )
        self.comments_df = self.comments_df.with_columns(
            pl.col("query_start_time").map_elements(self.timestamp_to_datetime_utc),
            pl.col("comment_created_utc").map_elements(self.timestamp_to_datetime_utc),
        )
        logger.info("Converted unix timestamp to an UTC datetime format")

    ### HELPERS
    def normalize_text_helper(self, txt: str) -> str:
        if txt is None:
            return None
        txt = norm.unicode(txt)
        txt = txt.lower()
        txt = rep.urls(txt, repl="<URL>")
        txt = rep.emails(txt, repl="<EMAIL>")
        txt = emoji.replace_emoji(txt, replace="<EMOJI>")
        txt = rmv.punctuation(txt)
        txt = norm.whitespace(txt)

        return txt
    
    def timestamp_to_datetime_utc(self, timestamp: float):
        return datetime.fromtimestamp(timestamp, timezone.utc)