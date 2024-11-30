from ..config.settings import settings
from ..models.investment_product import InvestmentProduct
from ..models.user_profile import InvestmentRecommendationRequest
from typing import List, Dict, Any
import pandas as pd
import json
import logging
from ..RagBase.rag_knowledge_base import RAGKnowledgeBase
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class InvestmentRecommenderService:
    def __init__(self, knowledge_base: RAGKnowledgeBase):
        """
        Initialize investment recommender service
        """
        self.knowledge_base = knowledge_base

        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=0.7
        )

        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["user_context", "semantic_context", "investment_context"],
            template="""
You are an AI Financial Advisor.

User Profile:
{user_context}

Semantic Insights:
{semantic_context}

Top Potential Investments:
{investment_context}

Generate a comprehensive, personalized investment recommendation that includes:
1. Investment allocation strategy
2. Specific investment recommendations
3. Risk management approach
4. Tax optimization strategies
5. Potential growth scenarios

The recommendation should be detailed, actionable, and tailored to the user's specific financial profile and goals.
"""
        )

        # Initialize the LLMChain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )

    async def generate_personalized_recommendation(
        self,
        user_profile: Dict[str, Any],
        investment_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Generate comprehensive investment recommendation using LLM
        """
        # Retrieve contextual insights
        semantic_context = self.knowledge_base.semantic_search(
            f"Investment strategy for {user_profile['age']} year old with {user_profile['risk_score']} risk tolerance"
        )

        # Get additional profile information
        additional_info = user_profile.get('user_profile', {})
        existing_investments = additional_info.get('existing_investments', [])
        investment_goals = additional_info.get('investment_goals', [])

        # Prepare user profile context with additional information
        user_context = f"""
- Age: {user_profile['age']}
- Risk Tolerance: {user_profile['risk_score']}/100
- Investment Horizon: {user_profile['time_horizon']} years
- Initial Investment: ₹{user_profile['initial_investment']:,}
- Target Amount: ₹{user_profile['target_amount']:,}
- Existing Investments: {', '.join(existing_investments) if existing_investments else 'None'}
- Investment Goals: {', '.join(investment_goals) if investment_goals else 'Not specified'}
"""

        # Prepare investment data context
        top_investments = self._select_top_investments(
            investment_data, 
            user_profile,
            existing_investments
        )
        investment_context = json.dumps(top_investments, indent=2)

        # Prepare the input for the chain
        chain_input = {
            "user_context": user_context,
            "semantic_context": json.dumps(semantic_context, indent=2),
            "investment_context": investment_context
        }

        # Generate recommendation using the chain
        recommendation = await self.chain.ainvoke(chain_input)
        recommendation_text = recommendation["text"]
        logging.info(f"Generated Recommendation: {recommendation_text}")

        return {
            "personalized_recommendation": recommendation_text,
            "semantic_context": semantic_context,
            "recommended_investments": top_investments
        }

    def _select_top_investments(
        self,
        investment_data: pd.DataFrame,
        user_profile: Dict[str, Any],
        existing_investments: List[str] = None,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Select top investments based on user profile and existing investments
        """
        if existing_investments is None:
            existing_investments = []

        # Apply scoring logic
        def calculate_investment_score(row):
            # Risk alignment (30% weight)
            risk_alignment = 30 * (1 - abs(row['risk_rating'] - (user_profile['risk_score'] / 100)))
            
            # Returns potential (25% weight)
            returns_score = 25 * row['returns']
            
            # Diversification score (20% weight)
            # Higher score if investment type is not in existing investments
            diversification_score = 20 * (1 if row['type'] not in existing_investments else 0.5)
            
            # Time horizon alignment (15% weight)
            time_horizon_score = 15 * (1 if row['recommended_horizon'] <= user_profile['time_horizon'] else 0.5)
            
            # Investment size compatibility (10% weight)
            min_investment = row.get('minimum_investment', 0)
            investment_size_score = 10 * (1 if min_investment <= user_profile['initial_investment'] else 0)
            
            return risk_alignment + returns_score + diversification_score + time_horizon_score + investment_size_score

        investment_data['score'] = investment_data.apply(calculate_investment_score, axis=1)
        top_investments = investment_data.nlargest(top_n, 'score').to_dict('records')
        return top_investments

    def generate_recommendation(
        self,
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive investment recommendation using the knowledge base
        """
        try:
            # Generate recommendation from knowledge base
            recommendation = self.knowledge_base.generate_comprehensive_recommendation(user_profile)
            
            # Add user profile to response
            recommendation["user_profile"] = user_profile
            
            logging.info(f"Generated Recommendation: {recommendation}")
            return recommendation
            
        except Exception as e:
            logging.error(f"Error generating recommendation: {str(e)}")
            raise
