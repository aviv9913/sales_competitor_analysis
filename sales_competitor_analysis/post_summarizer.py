from openai import OpenAI
import os

from sales_competitor_analysis.data_models.reddit_post import RedditPost
from sales_competitor_analysis.data_models.summarized_post import SummarizedPost
from sales_competitor_analysis.post_summarizer_prompt import PostSummarizerPrompt


class PostSummarizer:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            project=os.environ.get("OPENAI_PROJECT_ID"),
            organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
        )
        self.prompt = PostSummarizerPrompt()

    def summarize(self, post: RedditPost) -> SummarizedPost:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.prompt.get_system_message()},
                {"role": "user", "content": self.prompt.get_post_summarizer_prompt(post)},
            ],
            max_tokens=1000,
            response_format={"type": "json_object"},
        )

        summarized_post = SummarizedPost.model_validate_json(response.choices[0].message.content)
        summarized_post.id = post.id
        return summarized_post
