from datetime import datetime, timezone
from typing import Any, List

from sales_competitor_analysis.data_models.reddit_comment import RedditComment
from sales_competitor_analysis.data_models.json_base_model import JsonBaseModel


class RedditPost(JsonBaseModel):
    title: str
    text: str
    score: int
    creation_time_utc: str
    id: str
    url: str
    author_name: str
    comments: List[RedditComment]

    @classmethod
    def from_reddit(cls, reddit_post: Any, comments: List[RedditComment]) -> "RedditPost":
        """
        Creates a RedditPost instance from a PRAW Reddit submission object.

        Args:
            reddit_post (Any): A Reddit post object (e.g., from PRAW).

        Returns:
            RedditPost: An instance of RedditPost without comments.
            Comments require api calls to retrieve, hence handled separately.
        """
        return cls(
            title=reddit_post.title,
            text=reddit_post.selftext,
            score=reddit_post.score,
            creation_time_utc=datetime.fromtimestamp(reddit_post.created_utc, tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            id=reddit_post.id,
            url=reddit_post.url,
            author_name=reddit_post.author.name,
            comments=comments,
        )
