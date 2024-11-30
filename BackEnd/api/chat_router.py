from models.chat import ChatPrompt, ChatResponse
from services.chat_service import ChatService
from fastapi import APIRouter, HTTPException
from models.user_profile import InvestmentRecommendationRequest
from models.investment_response_model import InvestmentRecommendationResponse
from services.investment_recommender_service import InvestmentRecommenderService
from RagBase.rag_knowledge_base import RAGKnowledgeBase

router = APIRouter()
chat_service = ChatService()
knowledge_base = RAGKnowledgeBase()
investment_service = InvestmentRecommenderService(knowledge_base)

@router.post(
    "/chat",
    summary="Generate AI Chat Response",
    description="""
    Generate an AI response based on the user's prompt and optional context.
    
    The endpoint accepts a chat prompt and returns an AI-generated response using the configured LLM model.
    
    - Provide a clear prompt for the best results
    - Optional context can help guide the response
    - Responses are generated using GPT-3.5-turbo by default
    """,
    response_description="Returns the AI-generated response along with the original prompt"
)
async def chat_endpoint(
    chat_prompt: ChatPrompt
) -> str:
    """
    Generate an AI chat response.

    Args:
        chat_prompt (ChatPrompt): The user's prompt and optional context

    Returns:
        str: The AI-generated response and original prompt in plain text

    Raises:
        HTTPException: If there's an error generating the response
    """
    try:
        chat_response = await chat_service.generate_response(chat_prompt)
        # Convert the ChatResponse to a plain text string
        return f"Prompt: {chat_response.prompt}\nResponse: {chat_response.response}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/investment/recommendation",
    response_model=InvestmentRecommendationResponse,
    summary="Generate Investment Recommendation",
    description="""
    Generate a personalized investment recommendation based on the user's profile.

    The endpoint accepts a user profile and returns a detailed investment recommendation.

    - Provide accurate user profile information for the best results
    """,
    response_description="Returns the investment recommendation and related data"
)
async def investment_recommendation_endpoint(
    request: InvestmentRecommendationRequest
) -> InvestmentRecommendationResponse:
    """
    Generate an investment recommendation.

    Args:
        request (InvestmentRecommendationRequest): The user's profile

    Returns:
        InvestmentRecommendationResponse: The investment recommendation and related data

    Raises:
        HTTPException: If there's an error generating the recommendation
    """
    try:
        # Create user profile dictionary from request fields
        user_profile = {
            "age": request.age,
            "risk_score": request.risk_score,
            "time_horizon": request.time_horizon,
            "initial_investment": request.initial_investment,
            "target_amount": request.target_amount
        }
        
        # Add any additional user profile data if provided
        if request.user_profile:
            user_profile.update(request.user_profile)
            
        recommendation = investment_service.generate_recommendation(
            user_profile=user_profile
        )
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
