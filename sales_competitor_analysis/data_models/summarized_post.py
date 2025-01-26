from typing import List, Optional

from sales_competitor_analysis.data_models.json_base_model import JsonBaseModel


class SummarizedPost(JsonBaseModel):
    is_customer: bool
    summary: str
    competitor: str
    advantages: List[str]
    disadvantages: List[str]
    sentiment: str
    id: str = ""
