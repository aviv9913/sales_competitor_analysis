class ReportGeneratorPrompt:
    def get_system_message(self):
        return "You are an expert market analyzer in SentinelOne and you should provide a report based on processed reddit posts."

    def get_report_generation_prompt(
        self, top_3_competitors, best_advantages, best_disadvantages, overall_customer_satisfaction
    ):
        return f"""The posts have been summarized and aggregated to the following table:
1. top 3 competitors
2. best advantage
3. best disadvantages
4. overall customer satisfaction

You'll need to provide a full report explaining the findings based on the data.
You report should be consist of each summarization data and a brief explanation of the findings.
Add a conclusion at the end of the report with actionable insights.

The data is as follows:
1. Top 3 competitors
{top_3_competitors}
2. Best advantages
{best_advantages}
3. Best disadvantages
{best_disadvantages}
4. Overall customer satisfaction
{overall_customer_satisfaction}
"""
