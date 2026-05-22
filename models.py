from pydantic import BaseModel
from typing import List

class InputModel(BaseModel):
    category: str
    current_score:  float
    budget: int

class AlternativeProduct(BaseModel):
    name: str
    brand: str
    hormonal_health_score: float
    price_range: str
    free_from: List[str]
    purchase_links: List[str]