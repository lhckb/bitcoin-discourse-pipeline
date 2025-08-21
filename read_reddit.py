import praw
from dotenv import load_dotenv
import os
from logging_init import setup_logging
from time import time
from kafka import KafkaProducer
import json

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
        self.TOPIC_NAME="reddit_posts"
        self.ORIGIN = "reddit"
        self.kafka_producer = KafkaProducer(bootstrap_servers="localhost:9092")

    def query_reddit_for_discourse(self):
        query_results = []

        subreddit = self.reddit.subreddit("bitcoin+cryptocurrency+investing+btc+bitcoinmarkets+cryptotrading+cryptoinvesting+wallstreetbets+stocks+personalfinance")
        for post in subreddit.search("bitcoin OR btc", limit=100, time_filter="month", sort="new"): # TODO: UPDATE LIMIT WHEN READY
            logger.info(f"{post.title, post.id}")

            submission = self.reddit.submission(post.id)
            submission.comments.replace_more(limit=None, threshold=32) # get all MoreComments children if MoreComments contains >= 32 comments

            query_result = {
                "origin": self.ORIGIN,
                "query_start_time": query_start_time_utc,
                "post_id": post.id,
                "post_title": post.title,
                "post_created_utc": post.created_utc,
                "post_comments": [
                    {
                        "comment_id": comment.id,
                        "comment_body": comment.body,
                        "comment_created_utc": comment.created_utc    
                    }
                    for comment in submission.comments.list()
                ]
            }
            
            query_results.append(query_result)

            message = json.dumps(query_result).encode("utf-8")
            self.kafka_producer.send(self.TOPIC_NAME, message)  # TODO: check error
        
        self.kafka_producer.flush()
        return query_results

if __name__ == "__main__":
    reader = RedditReader()

    query_start_time_utc = time()

    results = reader.query_reddit_for_discourse()
    
    query_time_delta = time() - query_start_time_utc
    logger.info(f"Query ended in {query_time_delta} seconds")

    logger.info(f"Query produced {len(results)} results")