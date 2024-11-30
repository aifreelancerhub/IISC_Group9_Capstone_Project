from .investment_product import InvestmentProduct
from dataclasses import dataclass, asdict

@dataclass
class MutualFundInvestment(InvestmentProduct):
    category: str
    aum: float
    fund_manager: str
    fund_house: str
    tracking_error: float
    benchmark_index: str

    def to_dict(self):
        # Convert the dataclass to a dictionary
        return asdict(self)
