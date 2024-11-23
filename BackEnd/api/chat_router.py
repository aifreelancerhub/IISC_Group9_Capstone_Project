from fastapi import APIRouter, Depends, HTTPException
from ..models.chat import ChatPrompt, ChatResponse
from ..services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

@router.post(
    "/chat",
    response_model=ChatResponse,
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
) -> ChatResponse:
    """
    Generate an AI chat response.

    Args:
        chat_prompt (ChatPrompt): The user's prompt and optional context

    Returns:
        ChatResponse: The AI-generated response and original prompt

    Raises:
        HTTPException: If there's an error generating the response
    """
    try:
        return await chat_service.generate_response(chat_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
