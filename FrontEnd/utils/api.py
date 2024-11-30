import requests
import streamlit as st

class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8001"
    
    def chat_completion(self, prompt, temperature, top_p):
        """Generate chat completion"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "prompt": prompt,
                    "context": f"Temperature: {temperature}, Top_P: {top_p}"
                }
            )
            return response.json()
        except Exception as e:
            st.error(f"Error in chat completion: {str(e)}")
            return {"response": "cannot finish the request , some error happened"}

    def get_company_data(self, company_name):
        """Get company data"""
        try:
            response = requests.get(
                f"{self.base_url}/company/{company_name}"
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching company data: {str(e)}")
            return {}

    def get_fundamental_analysis(self, company_name):
        """Get fundamental analysis"""
        try:
            response = requests.get(
                f"{self.base_url}/company/{company_name}/fundamentals"
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching fundamental analysis: {str(e)}")
            return {}

    def get_technical_analysis(self, company_name, start_date, end_date):
        """Get technical analysis"""
        try:
            response = requests.get(
                f"{self.base_url}/company/{company_name}/technical",
                params={
                    "start_date": start_date,
                    "end_date": end_date
                }
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching technical analysis: {str(e)}")
            return {}

    def get_comparative_analysis(self, company_name, peer_companies):
        """Get comparative analysis"""
        try:
            response = requests.post(
                f"{self.base_url}/company/{company_name}/compare",
                json={
                    "peers": peer_companies
                }
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching comparative analysis: {str(e)}")
            return {}

    def get_market_overview(self):
        """Get market overview"""
        try:
            response = requests.get(
                f"{self.base_url}/market/overview"
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching market overview: {str(e)}")
            return {}

    def get_sector_analysis(self, sector):
        """Get sector analysis"""
        try:
            response = requests.get(
                f"{self.base_url}/market/sector/{sector}"
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching sector analysis: {str(e)}")
            return {}

    def get_recommendation(self, user_profile):
        """Get investment recommendation"""
        try:
            response = requests.post(
                f"{self.base_url}/investment/recommendation",
                json=user_profile  # Send fields directly
            )
            return response.json()
        except Exception as e:
            st.error(f"Error fetching investment recommendation: {str(e)}")
            return {}
