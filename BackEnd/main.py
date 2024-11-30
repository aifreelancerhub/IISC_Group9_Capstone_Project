from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat_router import router as chat_router
# from api.news_router import router as news_router

app = FastAPI(
    title="Financial Insights Chatbot API",
    description="""
    This API provides endpoints for generating AI chat responses and summarizing Nifty 20 news articles for investment insights.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
# app.include_router(news_router, prefix="/api/v1", tags=["News"])