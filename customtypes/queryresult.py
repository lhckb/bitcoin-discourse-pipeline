import dataclasses
from typing import List

@dataclasses.dataclass
class CommentData:
    def __init__(
        self,
        post_id: str,
        comment_id: str,
        comment_body: str,
        comment_created_utc: str
    ):
        self.comment_id = comment_id
        self.comment_body = comment_body
        self.comment_created_utc = comment_created_utc

@dataclasses.dataclass
class PostData:
    
    def __init__(
        self,
        origin: str,
        query_start_time: float,
        post_id: str,
        post_title: str,
        post_selftext: str,
        post_created_utc: float,
        post_comments: List[CommentData]
    ):
        self.origin = origin
        self.query_start_time = query_start_time
        self.post_id = post_id
        self.post_title = post_title
        self.post_selftext = post_selftext,
        self.post_created_utc = post_created_utc
        self.post_comments = post_comments


    def post_to_dict(self) -> dict:
        dict_object = {
            "origin": self.origin,
            "query_start_time": self.query_start_time,
            "post_id": self.post_id,
            "post_title": self.post_title,
            "post_selftext": self.post_selftext,
            "post_created_utc": self.post_created_utc,
        }

        return dict_object
    
    def post_comments_to_dict_list(self) -> List[dict]:
        list_object = [
            {
                "post_id": self.post_id,
                "comment_id": comment.comment_id,
                "comment_body": comment.comment_body,
                "comment_created_utc": comment.comment_created_utc    
            }
            for comment in self.post_comments
        ]
        
        return list_object