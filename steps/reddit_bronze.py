import praw
from dotenv import load_dotenv
import os
from utils.logging_init import setup_logging
from time import time
import json
from typing import List
from models.bronze import BronzePostData
from common.db import PGSQLConnector
import json

logger = setup_logging()
load_dotenv()

class RedditBronze:

    def __init__(self):
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit = praw.Reddit(
            user_agent="public bitcoin discourse extraction (by u/Medium-Dog-1310)",
            client_id=self.reddit_client_id,
            client_secret=self.reddit_client_secret,
        )
        self.ORIGIN = "reddit"
        self.connector = PGSQLConnector()

    def query_reddit_for_discourse(self) -> List[BronzePostData]:
        query_results = []

        query_start_time_utc = time()

        subreddit = self.reddit.subreddit("""
        bitcoin+cryptocurrency+investing+btc+bitcoinmarkets+cryptotrading+cryptoinvesting+wallstreetbets+stocks+personalfinance
        """)
        for post in subreddit.search("bitcoin OR btc", limit=5, time_filter="day", sort="new"): # TODO: UPDATE LIMIT WHEN READY (MAKE ARG)
            logger.info(f"{post.title, post.id}")

            post.comments.replace_more(limit=None)

            post_author = post.author.name if post.author else None

            query_result = BronzePostData(
                origin = self.ORIGIN,
                author = post_author,
                query_start_time = query_start_time_utc,
                post_id = post.id,
                post_title = post.title,
                post_selftext = post.selftext,
                post_created_utc = post.created_utc,
                post_comments = post.comments.list()
            )
            
            query_results.append(query_result)

        query_time_delta = time() - query_start_time_utc
        logger.info(f"Query ended in {query_time_delta} seconds")
        
        return query_results

    def insert_into_bronze_table(self, data: list[BronzePostData]):
        for obj in data:
            post = obj.post_to_dict()
            self.connector.insert("""
                INSERT INTO bronze_posts (
                    origin,
                    author,
                    query_start_time,
                    post_id,
                    post_title,
                    post_selftext,
                    post_created_utc,
                    post_comments
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
            """, (
                post["origin"],
                post["author"],
                post["query_start_time"],
                post["post_id"],
                post["post_title"],
                post["post_selftext"],
                post["post_created_utc"],
                json.dumps(post["comments"])
            ))