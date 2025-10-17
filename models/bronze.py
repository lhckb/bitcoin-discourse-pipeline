import dataclasses
from typing import List
from praw.models import Comment, MoreComments

@dataclasses.dataclass
class BronzePostData:
    
    def __init__(
        self,
        origin: str,
        author: str,
        query_start_time: float,
        post_id: str,
        post_title: str,
        post_selftext: str,
        post_created_utc: float,
        post_comments: List[Comment | MoreComments]
    ):
        self.origin = origin
        self.author = author
        self.query_start_time = query_start_time
        self.post_id = post_id
        self.post_title = post_title
        self.post_selftext = post_selftext
        self.post_created_utc = post_created_utc
        self.post_comments = post_comments


    def post_to_dict(self) -> dict:
        dict_object = {
            "origin": self.origin,
            "author": self.author,
            "query_start_time": self.query_start_time,
            "post_id": self.post_id,
            "post_title": self.post_title,
            "post_selftext": self.post_selftext,
            "post_created_utc": self.post_created_utc,
            "comments": [
                {
                    "comment_id": comment.id,
                    "comment_author": comment.author.name if comment.author else None,
                    "comment_body": comment.body,
                    "comment_created_utc": comment.created_utc    
                }
                for comment in self.post_comments
            ]
        }

        return dict_object