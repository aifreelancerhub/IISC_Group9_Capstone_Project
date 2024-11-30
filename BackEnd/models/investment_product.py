from dataclasses import dataclass

@dataclass
class InvestmentProduct:
    """Base class for investment products"""
    name: str
    type: str
    risk_score: float
    expected_returns: float
    expense_ratio: float
    tax_efficiency: float
