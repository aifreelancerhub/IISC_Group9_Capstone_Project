from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..config.settings import settings
from ..models.chat import ChatPrompt, ChatResponse
from .pdf_service import PDFService
import logging

class ChatService:
    def __init__(self):
        self.pdf_service = PDFService()
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["context", "prompt", "company_data", "fundamental_data"],
            template="""
            You are an AI Financial Advisor with access to stock market data and fundamental analysis.

            Available Company Data:
            {company_data}

            Fundamental Analysis:
            {fundamental_data}

            Additional Context: {context}

            User Question: {prompt}

            Please provide a detailed analysis and answer based on the available data. Include specific 
            references to financial metrics and fundamental analysis where relevant. Format your response 
            as a JSON object with keys: "ratios", "profitability", "financial_health", "growth_trends", 
            and "summary_metrics".

            Assistant: Let me help you with that analysis.
            """
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )
    
    def _get_relevant_company_data(self, prompt: str) -> tuple:
        """Get relevant company data based on the prompt"""
        companies = self.pdf_service.get_all_companies()
        relevant_company = None
        company_data = ""
        fundamental_data = ""

        for company in companies:
            if company.lower() in prompt.lower():
                relevant_company = company
                break
        
        if relevant_company:
            company_data = self.pdf_service.get_company_data(relevant_company)
            fundamental_data = self.pdf_service.get_fundamental_analysis(relevant_company)
        else:
            company_data = "General market data available for: " + ", ".join(companies)
            fundamental_data = "Please specify a company for detailed fundamental analysis."

        return company_data, fundamental_data
    
    async def generate_response(self, chat_prompt: ChatPrompt) -> ChatResponse:
        context = chat_prompt.context if chat_prompt.context else "No additional context provided."
        company_data, fundamental_data = self._get_relevant_company_data(chat_prompt.prompt)
        
        response = await self.chain.ainvoke({
            "context": context,
            "prompt": chat_prompt.prompt,
            "company_data": company_data,
            "fundamental_data": fundamental_data
        })
        logging.info(f"Raw LLM Response: {response['text']}")
        
        return ChatResponse(
            response=response["text"],
            prompt=chat_prompt.prompt
        )
