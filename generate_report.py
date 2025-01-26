import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

from sales_competitor_analysis.report_generator import ReportGenerator
from sales_competitor_analysis.data_models.reddit_post import RedditPost
from sales_competitor_analysis.data_models.summarized_post import SummarizedPost

POSTS_FOLDER_PATH = r"C:\repos\sales_competitor_analysis\posts"
SUMMARIZED_POSTS_FOLDER_PATH = r"C:\repos\sales_competitor_analysis\summarized_posts"


def read_summarized_posts_from_folder(folder):
    summarized_posts_dicts = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        summarized_post = SummarizedPost.load_from_json_file(file_path)
        summarized_posts_dicts.append(summarized_post.model_dump())

    df = pd.DataFrame(data=summarized_posts_dicts)
    return df


def read_posts_from_folder(folder):
    summarized_posts_dicts = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        summarized_post = RedditPost.load_from_json_file(file_path)
        summarized_posts_dicts.append(summarized_post.model_dump())

    df = pd.DataFrame(data=summarized_posts_dicts)
    return df


def get_posts_df():
    summarized_posts_df = read_summarized_posts_from_folder(SUMMARIZED_POSTS_FOLDER_PATH)
    posts_df = read_posts_from_folder(POSTS_FOLDER_PATH)
    df = pd.merge(summarized_posts_df, posts_df, on="id", how="inner")
    df["competitor"] = df["competitor"].str.lower()
    df["number_of_comments"] = df["comments"].apply(lambda x: len(x))

    return df


def generate_report(df):
    report_generator = ReportGenerator()
    report = report_generator.generate_report(df)
    Path("report.md").write_text(report)


def main():
    load_dotenv()
    df = get_posts_df()
    generate_report(df)


if __name__ == "__main__":
    main()
