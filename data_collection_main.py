from sales_competitor_analysis.reddit_data_collector import RedditDataCollector
from dotenv import load_dotenv


def main():
    load_dotenv()
    reddit_data_collector = RedditDataCollector(r"C:\repos\sales_competitor_analysis\data\posts")
    reddit_data_collector.collect_posts("Sentinel One", 20)


if __name__ == "__main__":
    main()
