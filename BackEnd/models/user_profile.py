from pydantic import BaseModel
from typing import Dict, Optional

class InvestmentRecommendationRequest(BaseModel):
    age: int
    risk_score: int
    time_horizon: int
    initial_investment: float
    target_amount: float
    user_profile: Optional[Dict] = None
