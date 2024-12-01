from fastapi import APIRouter, HTTPException
from services.news_service import NewsService
from models.news import NewsResponse, NewsItem  # Import the updated models
import pandas as pd

router = APIRouter()

news_service = NewsService()

@router.get("/news-summary", response_model=NewsResponse)
async def get_news_summary():
    """
    Fetch the top Nifty 20 company news, summarize it, and provide investment insights.
    """
    try:
        # Fetch news and generate summaries
        summary_df = await news_service.fetch_and_summarize_news()
        print(summary_df.head())  # To debug, check the fetched and summarized news

        # Convert each row of the summary_df into a NewsItem
        news_items = [
            NewsItem(
                company=row["company"],
                news_content=row["news_content"],  # Raw news content from your dataframe
                summary=row["summary"],    # Summary of the news
                datetime=row["datetime"]
            )
            for _, row in summary_df.iterrows()
        ]
        
        # Return the response in the required format
        return NewsResponse(data=news_items)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
