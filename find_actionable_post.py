from datetime import datetime, timedelta, timezone
import pandas as pd
import os
from dotenv import load_dotenv

from sales_competitor_analysis.action_chooser import ActionChooser
from sales_competitor_analysis.data_models.reddit_post import RedditPost
from sales_competitor_analysis.data_models.summarized_post import SummarizedPost

POSTS_FOLDER_PATH = r"C:\repos\sales_competitor_analysis\data\posts"
SUMMARIZED_POSTS_FOLDER_PATH = r"C:\repos\sales_competitor_analysis\data\summarized_posts"
ACTIONABLE_POSTS_FILE_PATH = r"C:\repos\sales_competitor_analysis\data\actionable_posts.json"


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
    df["creation_time_utc"] = pd.to_datetime(df["creation_time_utc"]).dt.tz_localize("UTC")

    return df


def filter_actionable_posts(df):
    actionable_posts = df.loc[
        (df["sentiment"] == "Negative")
        & (df["is_customer"])
        & (df["competitor"] != "")
        & (df["creation_time_utc"] > pd.to_datetime((datetime.now(timezone.utc) - timedelta(days=90))))
        & (df["number_of_comments"] > 5)
    ]

    actionable_posts = actionable_posts[
        [
            "id",
            "title",
            "summary",
            "competitor",
            "sentiment",
            "author_name",
            "creation_time_utc",
            "number_of_comments",
            "url",
        ]
    ]
    return actionable_posts


def main():
    load_dotenv()
    action_chooser = ActionChooser()
    df = get_posts_df()
    actionable_posts = filter_actionable_posts(df)
    actionable_posts["action_object"] = actionable_posts.apply(
        lambda x: action_chooser.choose_action(x.to_markdown()), axis=1
    )

    actionable_posts.to_json(ACTIONABLE_POSTS_FILE_PATH, index=False, orient="records", indent=4)


if __name__ == "__main__":
    main()
