from openai import OpenAI
import json
import os


class ActionChooser:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            project=os.environ.get("OPENAI_PROJECT_ID"),
            organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
        )

    def choose_action(self, post_md) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.get_system_message()},
                {
                    "role": "user",
                    "content": self.get_action_decider_prompt(post_md),
                },
            ],
            response_format={"type": "json_object"},
        )

        report_content = response.choices[0].message.content
        report = json.loads(report_content)
        return report

    def get_system_message(self) -> str:
        return """You are a top sales person who is analyzing reddit posts to support your customers.
    You'l receive a summary of a reddit post and you'l need to decide if the sales team should take action on it.
    If you choose to take action you'l need to provide a response to the customer.
    your output should be a json object with the following structure:
    {
        "take_action": True/False,
        "what_action": "what action to take, can be empty",
        "response": "your response to the customer"
    }
    
    Notes:
    - Your actions should be based on the information provided in the post.
    - Your response should be professional and helpful.
    - You can ask for more information if needed.
    - Your actions should be clear and concise.
    """

    def get_action_decider_prompt(self, post_md: str) -> str:
        return f"""Here's a summary of the reddit post:
    {post_md}"""
