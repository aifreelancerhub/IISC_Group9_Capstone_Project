from pydantic import BaseModel
from typing import Any, Dict, List

class InvestmentRecommendationResponse(BaseModel):
    user_profile: Dict[str, Any]
    investment_principles: List[Dict[str, Any]]
    total_investment: float
    asset_allocation: Dict[str, float]
    recommended_investments: Dict[str, Any]
    tax_optimization_strategies: List[str]
