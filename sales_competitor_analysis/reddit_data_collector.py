from typing import List
from numpy import save
import praw
import os
from pathlib import Path

from sales_competitor_analysis.data_models.reddit_comment import RedditComment
from sales_competitor_analysis.data_models.reddit_post import RedditPost
from sales_competitor_analysis.logger import get_logger


class RedditDataCollector:
    def __init__(self, posts_folder_path: str):
        self.logger = get_logger(__name__)
        self.reddit_client = praw.Reddit(
            client_id=os.environ["REDDIT_API_CLIENT_ID"],
            client_secret=os.environ["REDDIT_API_CLIENT_SECRET"],
            user_agent="YOUR_USER_AGENT",
        )
        self.subreddit = self.reddit_client.subreddit("msp")
        self.destination_path = posts_folder_path

    def collect_posts(self, query: str, limit: int) -> List[RedditPost]:
        posts_count = 0
        search_results = self.subreddit.search(query, sort="relevance", limit=limit)
        self.logger.info(f"Collecting posts for {query=}, {limit=}")
        for post in search_results:
            self.logger.info(f"Collecting data for {post.id=}, {post.url=}")
            comments = []
            post.comments.replace_more(limit=0)
            for comment in post.comments.list()[:10]:
                try:
                    reddit_comment = RedditComment.from_reddit(comment)
                    comments.append(reddit_comment)
                except Exception as e:
                    self.logger.error(f"Error processing {comment.id=}, {comment.body=}, {e=}")

            reddit_post = RedditPost.from_reddit(post, comments)
            path_str = f"{self.destination_path}/{post.id}.json"
            reddit_post.save_to_json_file(path_str)
            posts_count += 1

        self.logger.info(f"Collected {posts_count} posts")
