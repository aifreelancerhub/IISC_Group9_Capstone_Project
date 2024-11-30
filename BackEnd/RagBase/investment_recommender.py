from rag_knowledge_base import RAGKnowledgeBase

import pandas as pd
import json
from typing import List, Dict, Any
from openai import OpenAI

class LLMInvestmentRecommender:
    def __init__(self, knowledge_base: RAGKnowledgeBase):
        """
        Initialize LLM-based investment recommender
        """
        self.knowledge_base = knowledge_base
        
        # Initialize LLM Pipeline (replace with appropriate model)
        # self.llm_pipeline = pipeline('text-generation')
    
    def generate_personalized_recommendation(
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
        
        # Prepare user profile context
        user_context = f"""
        User Profile:
        - Age: {user_profile['age']}
        - Risk Tolerance: {user_profile['risk_score']}/100
        - Investment Horizon: {user_profile['time_horizon']} years
        - Initial Investment: ₹{user_profile['initial_investment']:,}
        - Target Amount: ₹{user_profile['target_amount']:,}
        """
        
        # Prepare investment data context
        top_investments = self._select_top_investments(investment_data, user_profile)
        investment_context = json.dumps(top_investments, indent=2)
        
        # Construct comprehensive prompt
        llm_prompt = f"""
        Context:
        {user_context}

        Semantic Insights:
        {json.dumps(semantic_context, indent=2)}

        Top Potential Investments:
        {investment_context}

        Generate a comprehensive, personalized investment recommendation 
        that includes:
        1. Investment allocation strategy
        2. Specific investment recommendations
        3. Risk management approach
        4. Tax optimization strategies
        5. Potential growth scenarios

        Recommendation should be detailed, actionable, and tailored to 
        the user's specific financial profile and goals.
        """
        
        # Generate recommendation using LLM
        recommendation = self._generate_llm_recommendation(llm_prompt)
        
        return {
            "personalized_recommendation": recommendation,
            "semantic_context": semantic_context,
            "recommended_investments": top_investments
        }
    
    def _select_top_investments(
        self, 
        investment_data: pd.DataFrame, 
        user_profile: Dict[str, Any], 
        top_n: int = 5
    ) -> List[Dict]:
        """
        Select top investments based on user profile
        """
        # Apply scoring logic similar to previous implementation
        def calculate_investment_score(row):
            risk_alignment = 30 * (1 - abs(row['risk_rating'] - (user_profile['risk_score'] / 100)))
            returns_score = 25 * row['returns']
            diversification_score = 20 * (1 if row['sector'] not in user_profile.get('existing_sectors', []) else 0.5)
            
            return risk_alignment + returns_score + diversification_score
        
        investment_data['score'] = investment_data.apply(calculate_investment_score, axis=1)
        top_investments = investment_data.nlargest(top_n, 'score').to_dict('records')
        
        return top_investments
    
    def _generate_llm_recommendation(self, prompt: str) -> str:
        """
        Generate recommendation using LLM
        """
        # In practice, replace with actual LLM call
        client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
            api_key="",
        )
        response = client.chat.completions.create(
        model="gpt-4",  # Specify the model to use
        messages=[
            {"role": "system", "content": "You are personal financial advisor."},  # System message to set the assistant's behavior
            {"role": "user", "content": prompt}                      # User input
        ],
        max_tokens=200,
        n=1,
        temperature=0.7
        )
        return response.choices[0].message.content.strip()
        # recommendation = self.llm_pipeline(prompt, max_length=1000)[0]['generated_text']
        # return recommendation