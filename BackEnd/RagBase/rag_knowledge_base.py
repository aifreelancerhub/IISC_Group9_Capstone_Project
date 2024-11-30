from models import (
    debt_fund_investment,
    mutual_fund_investment,
    stock_investment,
    store_type
)

import json
from typing import List, Dict, Any
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGKnowledgeBase:
    def __init__(self):
        """
        Initialize knowledge base with investment principles and data
        """
        self.investment_principles = [
            {
                "principle": "Asset Allocation Strategy",
                "description": "Dynamic asset allocation based on age, risk tolerance, and financial goals",
                "recommended_allocation": {
                    "low_risk": {"equity": "40-50%", "debt": "50-60%", "alternatives": "0-10%"},
                    "moderate_risk": {"equity": "60-70%", "debt": "30-40%", "alternatives": "0-10%"},
                    "high_risk": {"equity": "70-80%", "debt": "20-30%", "alternatives": "0-10%"}
                }
            },
            {
                "principle": "Risk Management",
                "description": "Gradual risk reduction as retirement approaches",
                "age_based_strategy": {
                    "20-35": "Aggressive growth",
                    "36-45": "Balanced growth",
                    "46-55": "Conservative growth",
                    "56+": "Capital preservation"
                }
            },
            {
                "principle": "Tax Optimization",
                "description": "Leverage tax-efficient investment vehicles",
                "strategies": [
                    "Use ELSS for tax deductions",
                    "Utilize long-term capital gains benefits",
                    "Consider tax-saving mutual funds"
                ]
            }
        ]
        
        # Sample Investment Products
        self.stocks = [
            stock_investment.StockInvestment(
                name="Reliance Industries Limited",
                symbol="RELIANCE",
                type="Equity",
                risk_score=0.7,
                expected_returns=0.12,
                sector="Oil & Gas",
                market_cap=1628000,
                pe_ratio=24.5,
                dividend_yield=1.2,
                beta=1.1,
                expense_ratio=0.01,
                tax_efficiency=0.8,
                key_strengths=["Diversified portfolio", "Strong retail and telecom presence"],
                potential_risks=["Regulatory challenges", "Global oil price volatility"]
            ),
            stock_investment.StockInvestment(
                name="HDFC Bank Limited",
                symbol="HDFCBANK",
                type="Equity",
                risk_score=0.5,
                expected_returns=0.14,
                sector="Banking",
                market_cap=1500000,
                pe_ratio=20.2,
                dividend_yield=1.8,
                beta=1.1,
                expense_ratio=0.01,
                tax_efficiency=0.7,
                key_strengths=["Strong retail banking", "Consistent growth"],
                potential_risks=["Regulatory changes"]
            ),
            stock_investment.StockInvestment(
                name="Infosys Limited",
                symbol="INFY",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.15,
                sector="IT",
                market_cap=750000,
                pe_ratio=23.5,
                dividend_yield=2.1,
                beta=0.9,
                expense_ratio=0.01,
                tax_efficiency=0.8,
                key_strengths=["Digital transformation", "Global client base"],
                potential_risks=["Tech sector volatility", "Currency fluctuations"]
            ),
            stock_investment.StockInvestment(
                name="ICICI Bank Limited",
                symbol="ICICIBANK",
                type="Equity",
                risk_score=0.55,
                expected_returns=0.13,
                sector="Banking",
                market_cap=1400000,
                pe_ratio=21.0,
                dividend_yield=1.6,
                beta=1.0,
                expense_ratio=0.01,
                tax_efficiency=0.75,
                key_strengths=["Strong retail growth", "Digital innovations"],
                potential_risks=["Economic slowdown"]
            ),
            stock_investment.StockInvestment(
                name="Tata Consultancy Services",
                symbol="TCS",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.14,
                sector="IT",
                market_cap=1300000,
                pe_ratio=29.3,
                dividend_yield=1.5,
                beta=0.8,
                expense_ratio=0.01,
                tax_efficiency=0.85,
                key_strengths=["Global delivery model", "Robust financials"],
                potential_risks=["Employee attrition"]
            ),
            stock_investment.StockInvestment(
                name="ITC Limited",
                symbol="ITC",
                type="Equity",
                risk_score=0.5,
                expected_returns=0.10,
                sector="FMCG",
                market_cap=582666.49,
                pe_ratio=24.5,
                dividend_yield=3.5,
                beta=0.8,
                expense_ratio=0.01,
                tax_efficiency=0.75,
                key_strengths=["Diversified product portfolio", "Strong brand recognition"],
                potential_risks=["Regulatory challenges in tobacco industry"]
            ),
            stock_investment.StockInvestment(
                name="Axis Bank Limited",
                symbol="AXISBANK",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.12,
                sector="Banking",
                market_cap=352882.80,
                pe_ratio=18.7,
                dividend_yield=1.2,
                beta=1.1,
                expense_ratio=0.01,
                tax_efficiency=0.70,
                key_strengths=["Robust retail banking", "Expanding digital services"],
                potential_risks=["Asset quality concerns"]
            ),
            stock_investment.StockInvestment(
                name="Larsen & Toubro Limited",
                symbol="LT",
                type="Equity",
                risk_score=0.55,
                expected_returns=0.11,
                sector="Construction",
                market_cap=486060.70,
                pe_ratio=20.0,
                dividend_yield=1.5,
                beta=1.0,
                expense_ratio=0.01,
                tax_efficiency=0.72,
                key_strengths=["Strong order book", "Diversified operations"],
                potential_risks=["Project execution delays"]
            ),
            stock_investment.StockInvestment(
                name="State Bank of India",
                symbol="SBIN",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.13,
                sector="Banking",
                market_cap=717584.07,
                pe_ratio=15.5,
                dividend_yield=2.0,
                beta=1.2,
                expense_ratio=0.01,
                tax_efficiency=0.70,
                key_strengths=["Extensive branch network", "Government backing"],
                potential_risks=["Non-performing assets"]
            ),
            stock_investment.StockInvestment(
                name="Bajaj Finance Limited",
                symbol="BAJFINANCE",
                type="Equity",
                risk_score=0.65,
                expected_returns=0.14,
                sector="Financial Services",
                market_cap=405404.87,
                pe_ratio=30.0,
                dividend_yield=0.8,
                beta=1.3,
                expense_ratio=0.01,
                tax_efficiency=0.68,
                key_strengths=["Strong retail lending", "Innovative financial products"],
                potential_risks=["Credit risk exposure"]
            ),
            stock_investment.StockInvestment(
                name="Asian Paints Limited",
                symbol="ASIANPAINT",
                type="Equity",
                risk_score=0.5,
                expected_returns=0.10,
                sector="Chemicals",
                market_cap=238060.14,
                pe_ratio=50.0,
                dividend_yield=1.0,
                beta=0.9,
                expense_ratio=0.01,
                tax_efficiency=0.75,
                key_strengths=["Market leadership", "Strong distribution network"],
                potential_risks=["Raw material price volatility"]
            ),
            stock_investment.StockInvestment(
                name="Bharti Airtel Limited",
                symbol="BHARTIARTL",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.12,
                sector="Telecommunications",
                market_cap=884553.82,
                pe_ratio=25.0,
                dividend_yield=1.5,
                beta=1.1,
                expense_ratio=0.01,
                tax_efficiency=0.70,
                key_strengths=["Large subscriber base", "Expanding 4G/5G services"],
                potential_risks=["Intense competition"]
            ),
            stock_investment.StockInvestment(
                name="HCL Technologies Limited",
                symbol="HCLTECH",
                type="Equity",
                risk_score=0.55,
                expected_returns=0.11,
                sector="IT",
                market_cap=504565.32,
                pe_ratio=20.0,
                dividend_yield=2.5,
                beta=0.9,
                expense_ratio=0.01,
                tax_efficiency=0.75,
                key_strengths=["Strong software services", "Global client base"],
                potential_risks=["Currency fluctuations"]
            ),
            stock_investment.StockInvestment(
                name="Maruti Suzuki India Limited",
                symbol="MARUTI",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.12,
                sector="Automobile",
                market_cap=346009.46,
                pe_ratio=35.0,
                dividend_yield=1.0,
                beta=1.0,
                expense_ratio=0.01,
                tax_efficiency=0.70,
                key_strengths=["Market leader in passenger vehicles", "Extensive dealer network"],
                potential_risks=["Economic downturns"]
            ),
            stock_investment.StockInvestment(
                name="Tata Steel Limited",
                symbol="TATASTEEL",
                type="Equity",
                risk_score=0.65,
                expected_returns=0.13,
                sector="Metals",
                market_cap=172111.50,
                pe_ratio=10.0,
                dividend_yield=2.0,
                beta=1.2,
                expense_ratio=0.01,
                tax_efficiency=0.68,
                key_strengths=["Integrated steel production", "Global presence"],
                potential_risks=["Cyclical industry risks"]
            )
        ]
        
        self.mutual_funds = [
            mutual_fund_investment.MutualFundInvestment(
                name="HDFC Balanced Advantage Fund",
                type="Hybrid",
                risk_score=0.5,
                expected_returns=0.12,
                category="Balanced",
                aum=50000,
                fund_manager="Fund Manager X",
                fund_house="HDFC Mutual Fund",
                expense_ratio=0.02,
                tax_efficiency=0.85,
                tracking_error=2.5,
                benchmark_index="NIFTY 50"
            ),
            mutual_fund_investment.MutualFundInvestment(
                name="SBI Bluechip Fund",
                type="Equity",
                risk_score=0.6,
                expected_returns=0.14,
                category="Large Cap",
                aum=75000,
                fund_manager="Fund Manager Y",
                fund_house="SBI Mutual Fund",
                expense_ratio=0.018,
                tax_efficiency=0.8,
                tracking_error=2.0,
                benchmark_index="NIFTY 50"
            )
        ]
        
        self.debt_funds = [
            debt_fund_investment.DebtFundInvestment(
                name="ICICI Prudential Gilt Fund",
                type="Debt",
                risk_score=0.2,
                expected_returns=0.07,
                duration="Long Term",
                credit_rating="AAA",
                govt_securities_percentage=80,
                corporate_bonds_percentage=20,
                expense_ratio=0.015,
                tax_efficiency=0.9
            ),
            debt_fund_investment.DebtFundInvestment(
                name="Axis Short Term Fund",
                type="Debt",
                risk_score=0.3,
                expected_returns=0.08,
                duration="Short Term",
                credit_rating="AA",
                govt_securities_percentage=40,
                corporate_bonds_percentage=60,
                expense_ratio=0.012,
                tax_efficiency=0.85
            )
        ]
         
        # Convert to vector store
        self.principal_vector_store = self._create_vector_store(
            self.investment_principles
        )
         # Convert to vector store
        self.mf_vector_store = self._create_vector_store_to_dict(
            self.mutual_funds
        )
         # Convert to vector store
        self.df_vector_store = self._create_vector_store_to_dict(
            self.debt_funds
        )
        self.stock_vector_store = self._create_vector_store_to_dict(
            self.stocks
        )
    
    def _create_vector_store(self, documents):
        """
        Create vector embeddings for semantic search
        """
        # Convert documents to text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = [json.dumps(doc) for doc in documents]
        
        # Create embeddings
        embeddings = OpenAIEmbeddings()  # Replace with appropriate embedding model
        vector_store = Chroma.from_texts(texts, embeddings)
        
        return vector_store
    
    def _create_vector_store_to_dict(self, documents):
        """
        Create vector embeddings for semantic search
        """
        # Convert documents to text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = [json.dumps(doc.to_dict()) for doc in documents]
        
        # Create embeddings
        embeddings = OpenAIEmbeddings()  # Replace with appropriate embedding model
        vector_store = Chroma.from_texts(texts, embeddings)
        
        return vector_store

    def semantic_search(self, query: str, k: int = 3, store: store_type.StoreType = store_type.StoreType.PRINCIPLE):
        """
        Perform semantic search on investment knowledge base
        """
        # if not self.vector_store:
        #     self.load_knowledge_sources()
        
        # Retrieve most relevant documents
        if store:
            if store ==  store_type.StoreType.PRINCIPLE:
                print("Searching in PRINCIPLE store")
                results = self.principal_vector_store.similarity_search(query, k=k)

            if store ==  store_type.StoreType.MF:
                print("Searching in MF store")
                results = self.mf_vector_store.similarity_search(query, k=k)

            if store ==  store_type.StoreType.DF:
                print("Searching in DF store")
                results = self.df_vector_store.similarity_search(query, k=k)

            if store ==  store_type.StoreType.STOCKS:
                print("Searching in STOCK store")
                results = self.stock_vector_store.similarity_search(query, k=k)

        else:
            raise ValueError("Invalid store type specified.")
        # results = store.similarity_search(query, k=k)
        return [json.loads(result.page_content) for result in results]

    
    def get_investment_principles(self, user_profile: Dict[str, Any]) -> List[Dict]:
        """
        Retrieve relevant investment principles based on user profile
        """
        # Risk-based principle selection
        risk_category = (
            "low_risk" if user_profile['risk_score'] < 40 else
            "moderate_risk" if 40 <= user_profile['risk_score'] < 70 else
            "high_risk"
        )
        
        # Age-based principle selection
        age_category = (
            "20-35" if user_profile['age'] < 35 else
            "36-45" if 35 <= user_profile['age'] < 46 else
            "46-55" if 46 <= user_profile['age'] < 56 else
            "56+"
        )
        
        relevant_principles = [
            principle for principle in self.investment_principles
            if risk_category in str(principle) or age_category in str(principle)
        ]
        
        return relevant_principles

    # Integrated Recommendation Methods
    def generate_comprehensive_recommendation(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive investment recommendation
        """
        # Retrieve relevant investment principles
        investment_principles = self.get_investment_principles(user_profile)
        
        # Calculate total investment amount
        total_investment = user_profile['initial_investment']
        
        # Risk-based asset allocation
        risk_allocation = self._determine_asset_allocation(user_profile)
        
        # Recommendation generation
        recommendation = {
            "user_profile": user_profile,
            "investment_principles": investment_principles,
            "total_investment": total_investment,
            "asset_allocation": risk_allocation,
            "recommended_investments": {
                "stocks": self._recommend_stocks(user_profile, risk_allocation['equity']),
                "mutual_funds": self._recommend_mutual_funds(user_profile, risk_allocation['debt']),
                "debt_funds": self._recommend_debt_funds(user_profile, risk_allocation['debt'])
            },
            "tax_optimization_strategies": self._get_tax_optimization_strategies(user_profile)
        }
        
        return recommendation

    def _determine_asset_allocation(self, user_profile: Dict[str, Any]) -> Dict[str, float]:
        """
        Determine asset allocation based on user profile
        """
        risk_score = user_profile['risk_score']
        
        # Simplified allocation logic
        if risk_score < 40:  # Conservative
            return {
                "equity": 0.4,  # 40%
                "debt": 0.55,   # 55%
                "alternatives": 0.05  # 5%
            }
        elif 40 <= risk_score < 70:  # Moderate
            return {
                "equity": 0.6,  # 60%
                "debt": 0.35,   # 35%
                "alternatives": 0.05  # 5%
            }
        else:  # Aggressive
            return {
                "equity": 0.7,  # 70%
                "debt": 0.25,   # 25%
                "alternatives": 0.05  # 5%
            }

    def _recommend_stocks(self, user_profile: Dict[str, Any], allocation_percentage: float) -> List[Dict[str, Any]]:
        """
        Recommend stocks based on user profile and allocation
        """
        # Filter stocks based on user risk profile
        filtered_stocks = [
            stock for stock in self.stocks
            if stock.risk_score <= user_profile['risk_score'] / 100
        ]
        
        # Sort stocks by expected returns and risk alignment
        sorted_stocks = sorted(
            filtered_stocks, 
            key=lambda x: (x.expected_returns, -abs(x.risk_score - user_profile['risk_score'] / 100)),
            reverse=True
        )
        
        # Select top stocks
        top_stocks = sorted_stocks[:3]
        
        if len(top_stocks) == 0:
            return []
        # Calculate investment amounts
        stock_investments = []
        remaining_amount = user_profile['initial_investment'] * allocation_percentage
        per_stock_amount = remaining_amount / len(top_stocks)
        
        for stock in top_stocks:
            stock_investment = {
                "name": stock.name,
                "symbol": stock.symbol,
                "investment_amount": per_stock_amount,
                "allocation_percentage": allocation_percentage * 100,
                "expected_returns": stock.expected_returns,
                "risk_score": stock.risk_score,
                "key_strengths": stock.key_strengths,
                "potential_risks": stock.potential_risks
            }
            stock_investments.append(stock_investment)
        
        return stock_investments

    def _recommend_mutual_funds(self, user_profile: Dict[str, Any], allocation_percentage: float) -> List[Dict[str, Any]]:
        """
        Recommend mutual funds based on user profile and allocation
        """
        # Filter mutual funds based on user risk profile
        filtered_funds = [
            fund for fund in self.mutual_funds
            if fund.risk_score <= user_profile['risk_score'] / 100
        ]
        
        # Sort funds by expected returns and risk alignment
        sorted_funds = sorted(
            filtered_funds, 
            key=lambda x: (x.expected_returns, -abs(x.risk_score - user_profile['risk_score'] / 100)),
            reverse=True
        )
        
        # Select top mutual funds
        top_funds = sorted_funds[:2]
        if len(top_funds) == 0:
            return []
        # Calculate investment amounts
        mutual_fund_investments = []
        remaining_amount = user_profile['initial_investment'] * allocation_percentage
        per_fund_amount = remaining_amount / len(top_funds)
        
        for fund in top_funds:
            fund_investment = {
                "name": fund.name,
                "fund_house": fund.fund_house,
                "investment_amount": per_fund_amount,
                "allocation_percentage": allocation_percentage * 100,
                "expected_returns": fund.expected_returns,
                "risk_score": fund.risk_score,
                "category": fund.category,
                "benchmark_index": fund.benchmark_index
            }
            mutual_fund_investments.append(fund_investment)
        
        return mutual_fund_investments

    def _recommend_debt_funds(self, user_profile: Dict[str, Any], allocation_percentage: float) -> List[Dict[str, Any]]:
        """
        Recommend debt funds based on user profile and allocation
        """
        # Filter debt funds based on user risk profile
        filtered_funds = [
            fund for fund in self.debt_funds
            if fund.risk_score <= user_profile['risk_score'] / 100
        ]
        
        # Sort funds by expected returns and risk alignment
        sorted_funds = sorted(
            filtered_funds, 
            key=lambda x: (x.expected_returns, -abs(x.risk_score - user_profile['risk_score'] / 100)),
            reverse=True
        )
        
        # Select top debt funds
        top_funds = sorted_funds[:2]
        if len(top_funds) == 0:
            return []
        # Calculate investment amounts
        debt_fund_investments = []
        remaining_amount = user_profile['initial_investment'] * allocation_percentage
        per_fund_amount = remaining_amount / len(top_funds)
        
        for fund in top_funds:
            fund_investment = {
                "name": fund.name,
                "investment_amount": per_fund_amount,
                "allocation_percentage": allocation_percentage * 100,
                "expected_returns": fund.expected_returns,
                "risk_score": fund.risk_score,
                "duration": fund.duration,
                "credit_rating": fund.credit_rating,
                "govt_securities_percentage": fund.govt_securities_percentage,
                "corporate_bonds_percentage": fund.corporate_bonds_percentage
            }
            debt_fund_investments.append(fund_investment)
        
        return debt_fund_investments

    def _get_tax_optimization_strategies(self, user_profile: Dict[str, Any]) -> List[str]:
        """
        Generate tax optimization strategies
        """
        tax_strategies = [
            "Utilize ELSS for tax deductions under Section 80C",
            "Consider long-term capital gains tax benefits",
            "Optimize debt fund investments for tax efficiency"
        ]
        
        return tax_strategies
