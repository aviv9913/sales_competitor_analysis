from typing import Any
from pydantic import BaseModel
from datetime import datetime, timezone


class RedditComment(BaseModel):
    id: str
    text: str
    score: int
    author_name: str
    creation_time_utc: str

    @classmethod
    def from_reddit(cls, reddit_comment: Any) -> "RedditComment":
        """
        Creates a RedditComment instance from a PRAW Reddit comment object.

        Args:
            reddit_comment (Any): A Reddit comment object (e.g., from PRAW).

        Returns:
            RedditComment: An instance of RedditComment.
        """
        return cls(
            id=reddit_comment.id,
            text=reddit_comment.body,
            score=reddit_comment.score,
            author_name=reddit_comment.author.name,
            creation_time_utc=datetime.fromtimestamp(reddit_comment.created_utc, tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )
