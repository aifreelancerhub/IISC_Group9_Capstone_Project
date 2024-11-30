import pandas as pd
import numpy as np
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from sentence_transformers import SentenceTransformer
import re
import openai
import faiss
from dataclasses import asdict
from enum import Enum

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import JSONLoader
from transformers import pipeline
from openai import OpenAI



class InvestmentRecommendationEngine:
    def __init__(self, knowledge_base: RAGKnowledgeBase):
        """
        Initialize recommendation engine with knowledge base
        """
        self.knowledge_base = knowledge_base

    def generate_comprehensive_recommendation(
        self, 
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive investment recommendation
        """
        # Retrieve relevant investment principles
        investment_principles = self.knowledge_base.get_investment_principles(user_profile)
        
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
    
    def _recommend_stocks(
        self, 
        user_profile: Dict[str, Any], 
        allocation_percentage: float
    ) -> List[Dict[str, Any]]:
        """
        Recommend stocks based on user profile and allocation
        """
        # Filter stocks based on user risk profile
        filtered_stocks = [
            stock for stock in self.knowledge_base.stocks
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
            return[]
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
    
    def _recommend_mutual_funds(
        self, 
        user_profile: Dict[str, Any], 
        allocation_percentage: float
    ) -> List[Dict[str, Any]]:
        """
        Recommend mutual funds based on user profile and allocation
        """
        # Filter mutual funds based on user risk profile
        filtered_funds = [
            fund for fund in self.knowledge_base.mutual_funds
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
            return[]
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
    
    def _recommend_debt_funds(
        self, 
        user_profile: Dict[str, Any], 
        allocation_percentage: float
    ) -> List[Dict[str, Any]]:
        """
        Recommend debt funds based on user profile and allocation
        """
        # Filter debt funds based on user risk profile
        filtered_funds = [
            fund for fund in self.knowledge_base.debt_funds
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

def generate_financial_recommendation(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive financial recommendation
    """
    # Initialize knowledge base
    knowledge_base = RAGKnowledgeBase()
    
    # Initialize recommendation engine
    recommendation_engine = InvestmentRecommendationEngine(knowledge_base)
    
    # Generate recommendation
    recommendation = recommendation_engine.generate_comprehensive_recommendation(user_profile)
    
    return recommendation

def generate_financial_recommendation1(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    # Search for relevant investments
    query = f"Low-risk investments for a {user_profile['age']} year old with a {user_profile['risk_score']} risk score."
    knowledge_base = RAGKnowledgeBase()
    # relevant_investments = knowledge_base.semantic_search(query, k = 3, store = store_type.StoreType.PRINCIPLE)

    # print(relevant_investments)
    
    # Initialize recommendation engine
    recommendation_engine = LLMInvestmentRecommender(knowledge_base)
    # Generate personalized recommendations using LLM
    personalized_advice = recommendation_engine.generate_personalized_recommendation(user_profile, investment_data)
    recommendation_engine = InvestmentRecommendationEngine(knowledge_base)
    
    # Generate recommendation
    recommendation = recommendation_engine.generate_comprehensive_recommendation(user_profile)

    
    return {
        "user_profile": user_profile,
        "recommended_investments": recommendation,
        "personalized_advice": personalized_advice
    }
# Example Usage
user_profile = {
    'age': 60,
    'risk_score': 59,  # Moderate to High Risk
    'time_horizon': 10,
    'initial_investment': 1000000,  # ₹10,00,000
    'target_amount': 10000000  # ₹1,00,00,000
}
# Simulate investment data
investment_data = pd.DataFrame({
    'name': ['Tech Fund', 'Blue Chip Fund', 'Sectoral Fund'],
    'risk_rating': [0.6, 0.5, 0.7],
    'returns': [0.12, 0.10, 0.15],
    'sector': ['Technology', 'Bluechip', 'Sectoral']
})

# Generate Financial Recommendation
financial_recommendation = generate_financial_recommendation1(user_profile)
print(financial_recommendation["personalized_advice"])
print("===============================")
print(financial_recommendation["recommended_investments"])

# Convert to JSON for easy readability
# print(json.dumps(financial_recommendation, indent=2))
