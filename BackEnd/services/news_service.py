import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.settings import settings
from scraper.news_scraper import NewsScraper

class NewsService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=0.7
        )
        self.summary_template = PromptTemplate(
            input_variables=["company", "news_content"],
            template="""\
            Company: {company}
            News Content: {news_content}

            Please summarize this news article in 100 words and identify if the news is positive, negative, or neutral for investment.
            Provide an investment recommendation in 50 words with heading.
            Provide indent of news with heading
            """
        )
        self.summary_chain = LLMChain(llm=self.llm, prompt=self.summary_template)

    async def fetch_and_summarize_news(self) -> pd.DataFrame:
        """
        Fetch news and generate summarized insights for each headline.
        """
        scraper = NewsScraper()
        news_df = scraper.fetch_news()
        #print(news_df)
        summaries = []
        for _, row in news_df.iterrows():
            response = await self.summary_chain.ainvoke({
                "company": row["company"],
                "news_content": row["news"]  # Use 'news' content now instead of headline
            })
            #print(type(response))
            #print(response)
            summaries.append({
                "company": row["company"],
                "news_content": row["news"],  # Storing the raw content
                "summary": response["text"],
                "datetime": row["datetime"],
            })

        return pd.DataFrame(summaries)
