import praw
from dotenv import load_dotenv
import os
from utils.logging_init import setup_logging
from time import time
import json
from typing import List
from customtypes.queryresult import PostData, CommentData
from utils.constants import Constants

logger = setup_logging()

class RedditReader:

    def __init__(self):
        load_dotenv()
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit = praw.Reddit(
            user_agent="public bitcoin discourse extraction (by u/Medium-Dog-1310)",
            client_id=self.reddit_client_id,
            client_secret=self.reddit_client_secret,
        )
        self.TOPIC_NAME = Constants.REDDIT_RAW_TOPIC_NAME.value
        self.ORIGIN = "reddit"

    def query_reddit_for_discourse(self, query_start_time_utc: float) -> List[PostData]:
        query_results = []

        subreddit = self.reddit.subreddit("bitcoin+cryptocurrency+investing+btc+bitcoinmarkets+cryptotrading+cryptoinvesting+wallstreetbets+stocks+personalfinance")
        for post in subreddit.search("bitcoin OR btc", limit=5, time_filter="month", sort="new"): # TODO: UPDATE LIMIT WHEN READY (MAKE ARG)
            logger.info(f"{post.title, post.id}")

            submission = self.reddit.submission(post.id)
            submission.comments.replace_more(limit=None, threshold=32) # get all MoreComments children if MoreComments contains >= 32 comments

            query_result = PostData(
                origin = self.ORIGIN,
                query_start_time = query_start_time_utc,
                post_id = post.id,
                post_title = post.title,
                post_selftext = post.selftext,
                post_created_utc = post.created_utc,
                post_comments = [
                    CommentData(
                        post_id = post.id,
                        comment_id = comment.id,
                        comment_body = comment.body,
                        comment_created_utc = comment.created_utc
                    )
                    for comment in submission.comments.list()
                ]
            )
            
            query_results.append(query_result)
        
        return query_results
