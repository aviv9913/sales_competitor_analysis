import re
from openai import OpenAI
import os

from sales_competitor_analysis.report_generator_prompt import ReportGeneratorPrompt


class ReportGenerator:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            project=os.environ.get("OPENAI_PROJECT_ID"),
            organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
        )
        self.prompt = ReportGeneratorPrompt()

    def generate_report(self, df) -> str:
        top_3_competitors = self._get_top_3_competitors(df)
        best_advantages = self._get_best_advantages(df)
        best_disadvantages = self._get_best_disadvantages(df)
        overall_customer_satisfaction = self._get_overall_customer_satisfaction(df)

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.prompt.get_system_message()},
                {
                    "role": "user",
                    "content": self.prompt.get_report_generation_prompt(
                        top_3_competitors.to_markdown(),
                        best_advantages.to_markdown(),
                        best_disadvantages.to_markdown(),
                        overall_customer_satisfaction.to_markdown(),
                    ),
                },
            ],
        )

        report_content = response.choices[0].message.content
        return report_content

    def _get_top_3_competitors(self, df):
        return (
            df.loc[(df["competitor"] != "") & (df["sentiment"] == "Negative")]
            .groupby("competitor")
            .agg({"number_of_comments": "sum", "score": "sum"})
            .sort_values(by="score", ascending=False)
            .head(3)
        )

    def _get_best_advantages(self, df):
        return (
            df.explode("advantages")
            .groupby("advantages")
            .agg({"score": "sum", "competitor": lambda x: set([item for item in x if item != ""]), "summary": "first"})
            .sort_values(by="score", ascending=False)
            .head(3)
        )

    def _get_best_disadvantages(self, df):
        return (
            df.explode("disadvantages")
            .groupby("disadvantages")
            .agg({"score": "sum", "competitor": lambda x: set([item for item in x if item != ""]), "summary": "first"})
            .sort_values(by="score", ascending=False)
            .head(3)
        )

    def _get_overall_customer_satisfaction(self, df):
        return (
            df.loc[df["is_customer"]]
            .groupby("sentiment")
            .agg({"score": "sum", "id": "count"})
            .rename(columns={"id": "count"})
        )
