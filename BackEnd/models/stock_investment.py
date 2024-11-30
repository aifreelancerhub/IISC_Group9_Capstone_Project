from models.investment_product import InvestmentProduct
from dataclasses import dataclass, asdict

@dataclass
class StockInvestment(InvestmentProduct):
    sector: str
    market_cap: float
    pe_ratio: float
    dividend_yield: float
    beta: float
    symbol : str
    key_strengths: list
    potential_risks: list

    def to_dict(self):
        # Convert the dataclass to a dictionary
        return asdict(self)
