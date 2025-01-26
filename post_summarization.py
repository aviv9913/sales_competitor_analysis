from dotenv import load_dotenv
import os

from sales_competitor_analysis.data_models.reddit_post import RedditPost
from sales_competitor_analysis.post_summarizer import PostSummarizer


def main():
    load_dotenv()
    post_summarizer = PostSummarizer()
    folder_path = r"C:\repos\sales_competitor_analysis\data\posts"
    for post_json_file_name in os.listdir(folder_path):
        print(f"Summarizing post from {post_json_file_name}")
        try:
            post_json_file_path = os.path.join(folder_path, post_json_file_name)
            post = RedditPost.load_from_json_file(post_json_file_path)
            summarized_post = post_summarizer.summarize(post)
            summarized_post_json_file_path = os.path.join(
                r"C:\repos\sales_competitor_analysis\data\summarized_posts", f"{summarized_post.id}_summary.json"
            )
            summarized_post.save_to_json_file(summarized_post_json_file_path)
        except Exception as e:
            print(f"Failed to summarize post {post_json_file_name}: {e}")


if __name__ == "__main__":
    main()
