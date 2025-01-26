from sales_competitor_analysis.data_models.reddit_post import RedditPost


class PostSummarizerPrompt:
    def get_post_summarizer_prompt(self, post: RedditPost):
        return f"""Title: "{post.title}" \nText: "{post.text}" """

    def get_system_message(self):
        return """# Overview
You are tasked with summarizing a Reddit post related to SentinelOne and its competitors. Analyze the title and post text to extract key information useful for the marketing team. Follow the instructions carefully and structure the output as a JSON object.

# Instructions:
## Customer Status: Determine whether the poster is a customer of SentinelOne.
Output as `is_customer`: `True` or `is_customer`: `False`.

## Text Summary: Provide a brief summary of the post in one or two sentences.
Focus on the main situation or issue discussed.

## Competitor: Identify SentinelOne's competitor mentioned in the post.
Not all posts will mention a competitor.
Posts may mention multiple companies but focus only on the primary competitor.
Output as "competitor": "<Competitor Name>". If none is mentioned, use "competitor": "".

## Advantages of SentinelOne: List any advantages of SentinelOne over the competitor mentioned in the post.
Use only phrases from the following list:
* "Security Features"
* "Security Performance"
* "User-Friendly Interface"
* "Ease of Deployment"
* "Scalability"
* "Cross-Platform Support"
* "Visibility"
* "Customer Support"
* "Integration"
* "Cost"

If none are explicitly mentioned, leave as "advantages": [].

## Disadvantages of SentinelOne: List any disadvantages of SentinelOne over the competitor mentioned in the post.
Use only phrases from the following list:
* "Security Features"
* "Security Performance"
* "User-Friendly Interface"
* "Ease of Deployment"
* "Scalability"
* "Cross-Platform Support"
* "Visibility"
* "Customer Support"
* "Integration"
* "Cost"

If none are explicitly mentioned, leave as "disadvantages": [].

## Post Sentiment: Determine whether the post is in favor of SentinelOne, the competitor, or neutral.
Output as "sentiment": "Positive", "sentiment": "Negative", or "sentiment": "Neutral".

# Example:
## Input
Title: "Ninja Forcing Us to Pay $20,000 for SentinelOne License"
Text: "I need to vent about a frustrating situation we're dealing with at work. My colleague recently tried to *test* SentinelOne, which we apparently \"purchased\" through Ninja. Somehow, this turned into a $20,000 charge! The kicker? In our country, only a CEO can legally sign off on purchases of this nature. My colleague certainly doesn't have that authority.\n\nWe reached out to Ninja to explain the situation, but they're insisting we pay up. This seems ridiculous given the circumstances. Has anyone else dealt with something like this?\n\nHonestly, it feels like we're being strong-armed into paying for something we never intended to buy in the first place. \n\nUpdate:\n\nQuick update on the situation: I spoke with a representative from Ninja, and they were very understanding. We clarified the misunderstanding, and they agreed to remove the claim. Ninja handled it professionally, and I appreciate how cool they've been about the whole thing.\n\nI also want to clarify that we share a lot of the blame here. Ninja has been very professional about handling the situation. I'm glad we were able to resolve this amicably.\n\nThe big takeaway here is that we probably should have escalated the issue to the right person sooner.\nLesson learned! Thanks to everyone who offered advice and support!"

## Output:
{
  "is_customer": "False",
  "summary": "The poster describes a misunderstanding where their company was charged $20,000 for a SentinelOne license through Ninja, which was resolved amicably after discussions.",
  "competitor": "",
  "advantages": ["Customer Support"],
  "disadvantages": ["Cost"],
  "sentiment": "Natural"
}

# Notes:
Be concise in your output, but ensure all key details are captured.
If multiple competitors are mentioned, list only the primary one.
For advantages/disadvantages, infer based on explicit comparisons or implied sentiments in the text."""
