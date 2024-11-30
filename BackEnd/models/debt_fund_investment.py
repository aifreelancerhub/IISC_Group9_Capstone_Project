from models.investment_product import InvestmentProduct
from dataclasses import dataclass, asdict
@dataclass
class DebtFundInvestment(InvestmentProduct):
    duration: str
    credit_rating: str
    govt_securities_percentage: float
    corporate_bonds_percentage: float

    def to_dict(self):
        # Convert the dataclass to a dictionary
        return asdict(self)
