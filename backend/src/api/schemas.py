from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    crop: str
    market: str


class AdvisorySchema(BaseModel):
    title: str
    body: str
    steps: List[str]
    color: str


class PriceTrendPoint(BaseModel):
    date: str
    price: int


class AnalysisResponse(BaseModel):
    projected_price: int
    baseline_price: int
    target_date: str
    historical_norm: int
    risk_level: str
    risk_score: int
    price_change: float
    weather_source: str
    message: str
    advisory: AdvisorySchema
    timeline: List[Dict[str, Any]]
    price_trend: List[PriceTrendPoint]


class MarketsResponse(BaseModel):
    markets: List[str]
