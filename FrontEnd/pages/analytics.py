import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from IISC_Group9_Capstone_Project.FrontEnd.utils.api import APIClient
from IISC_Group9_Capstone_Project.BackEnd.services.pdf_service import PDFService

class AnalyticsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.pdf_service = PDFService()

    def render(self, authentication_status):
        # if not authentication_status:
        #     st.warning("You need to log in to access the Analytics page.")
        #     return

        st.title("Stock Market Analytics")
        companies = self.pdf_service.get_all_companies()
        selected_company = st.selectbox("Select Company", companies)
        analysis_type = st.radio(
            "Select Analysis Type",
            ["Technical Analysis", "Fundamental Analysis", "Comparative Analysis"]
        )

        if analysis_type == "Technical Analysis":
            self._render_technical_analysis(selected_company)
        elif analysis_type == "Fundamental Analysis":
            self._render_fundamental_analysis(selected_company)
        else:
            self._render_comparative_analysis(selected_company)

    def _render_technical_analysis(self, company):
        st.subheader("Technical Analysis")
    
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        indicators = st.multiselect(
            "Select Technical Indicators",
            ["Moving Average", "RSI", "MACD", "Bollinger Bands"],
            default=["Moving Average"]
        )

        if st.button("Generate Technical Analysis"):
            company_data = self.pdf_service.get_company_data(company)
            st.text_area("Technical Data", company_data.get('text', ''), height=300)

            fig = go.Figure()
            
            dates = pd.date_range(start=start_date, end=end_date)
            prices = pd.Series(range(len(dates))) + 100
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=prices,
                mode='lines',
                name='Stock Price'
            ))
            
            fig.update_layout(
                title=f"{company} Technical Analysis",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Technical Indicators Summary")
            indicators_df = pd.DataFrame({
                'Indicator': ['RSI', 'MACD', 'MA(50)', 'MA(200)'],
                'Value': ['65.5', '12.3', '495.0', '482.0'],
                'Signal': ['Neutral', 'Buy', 'Buy', 'Buy']
            })
            st.dataframe(indicators_df, use_container_width=True)

    def _render_fundamental_analysis(self, company):
        st.subheader("Fundamental Analysis")
        company_data = self.pdf_service.get_company_data(company)
        if company_data:
            st.metric("Market Cap", f"₹{company_data.get('Market Cap', 'N/A')}")
            st.metric("P/E Ratio", company_data.get('PE Ratio', 'N/A'))
            st.metric("Book Value", company_data.get('Book Value', 'N/A'))
            st.metric("Dividend Yield", company_data.get('Dividend Yield', 'N/A'))
            st.metric("Debt to Equity", company_data.get('Debt to Equity', 'N/A'))
            st.metric("ROE", company_data.get('ROE', 'N/A'))
            st.metric("Revenue Growth", company_data.get('Revenue Growth', 'N/A'))
            st.metric("Operating Margin", company_data.get('Operating Margin', 'N/A'))
            st.metric("EPS", company_data.get('EPS', 'N/A'))
            st.metric("Price to Sales Ratio", company_data.get('Price to Sales Ratio', 'N/A'))
            st.metric("Current Ratio", company_data.get('Current Ratio', 'N/A'))
            st.metric("Quick Ratio", company_data.get('Quick Ratio', 'N/A'))
            st.metric("Free Cash Flow", company_data.get('Free Cash Flow', 'N/A'))
        else:
            st.warning("No fundamental data available for this company.")

    def _render_comparative_analysis(self, company):
        st.subheader("Comparative Analysis")

        peers = st.multiselect(
            "Select Peers for Comparison",
            ["TCS", "INFY", "WIPRO", "HCLTECH"],
            default=["TCS", "INFY"]
        )

        if st.button("Generate Comparison"):
            metrics = ['P/E Ratio', 'Market Cap', 'Revenue Growth', 'Profit Margin']
            companies = [company] + peers
            
            fig = go.Figure()
            
            for metric in metrics:
                fig.add_trace(go.Bar(
                    name=metric,
                    x=companies,
                    y=[25, 28, 22, 24],
                    text=['25x', '28x', '22x', '24x'],
                    textposition='auto',
                ))

            fig.update_layout(
                title="Peer Comparison",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Detailed Comparison")
            comparison_df = pd.DataFrame({
                'Metric': metrics,
                company: ['25x', '₹150,000 Cr', '15%', '12.5%'],
                'Industry Avg': ['24x', '₹125,000 Cr', '12%', '11%']
            })
            st.dataframe(comparison_df, use_container_width=True)
