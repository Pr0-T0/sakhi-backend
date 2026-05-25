from pydantic import BaseModel,Field
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

class InsightRequest(BaseModel):
    avg_nutrition_score: float = Field(...,ge=0, le=100)
    avg_toxicity_score: float = Field(...,ge=0, le=100)
    avg_processed_score: float = Field(...,ge=0,le=100)
    avg_hormonal_score: float = Field(...,ge=0,le=100)
    avg_overall_score: float = Field(...,ge=0,le=100)
    scan_frequency_weekly: float = Field(...,ge=0)
    scan_count: int = Field(...,ge=0)
    healthy_scan_ratio: float = Field(...,ge=0,le=1)
    high_toxicity_ratio: float = Field(...,ge=0,le=1)
    cosmetic_ratio: float = Field(...,ge=0,le=1)
    food_ratio: float = Field(...,ge=0,le=1)

class PredictionItem(BaseModel):
    label: str
    confidenc: float
class InsightResponse(BaseModel):
    predictions: list[PredictionItem]
