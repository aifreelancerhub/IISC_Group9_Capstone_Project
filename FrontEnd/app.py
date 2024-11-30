import streamlit as st
from streamlit_option_menu import option_menu
from utils.api import APIClient
from pages.chat import ChatPage
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from fpdf import FPDF
import json
import io
from utils.auth import Authentication

st.set_page_config(
    page_title="Financial Advisor Dashboard",
    page_icon="💼",
    layout="wide"
)

def create_metric_card(title, value, description):
    with st.container():
        st.markdown(f"""
        <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; margin-bottom: 1rem;">
            <h3>{title}</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{value}</p>
            <p style="font-size: 0.9rem; color: #666;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

def create_radar_plot(data):
    categories = ['P/E Ratio', 'ROE', 'Net Profit Margin', 'Operating Margin', 'Debt/Equity']
    values = [0.7, 0.8, 0.6, 0.75, 0.65]  # Example values, should be extracted from actual data
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Financial Metrics'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )
    return fig

def create_trend_plot(data):
    # Example trend data - should be replaced with actual data
    df = pd.DataFrame({
        'Period': ['Q1', 'Q2', 'Q3', 'Q4'],
        'Revenue': [100, 120, 115, 130],
        'Profit': [20, 25, 23, 28]
    })
    
    fig = px.line(df, x='Period', y=['Revenue', 'Profit'], title='Financial Trends')
    return fig

def generate_pdf_report(analysis_text, figures):
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Financial Analysis Report', ln=True, align='C')
    
    # Add analysis text
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, analysis_text)
    
    # Add plots
    for fig in figures:
        img_bytes = fig.to_image(format="png")
        pdf.image(io.BytesIO(img_bytes), x=10, y=None, w=190)
    
    return pdf.output(dest='S').encode('latin1')

def main():
    auth = Authentication()
    name, authentication_status, username = auth.authenticate()
    if authentication_status:
        with st.sidebar:
            st.write(f"Welcome, {name}")
            auth.logout()
            st.title("Configuration")
            
            # Radio buttons for mode selection
            mode = st.radio("Select Mode", ("Recommendation", "Chat"))
            
            # Initialize temperature and top_p
            temperature = 0.7
            top_p = 0.9
            
            api_client = APIClient()  # Initialize APIClient here
            
            if mode == "Recommendation":
                # Enable inputs for recommendation
                temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
                top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1)
                st.markdown("### User Profile")
                age = st.slider("Age", 18, 100, 60, 1)
                risk_score = st.slider("Risk Score", 0, 100, 59, 1)
                time_horizon = st.slider("Time Horizon (Years)", 1, 50, 10, 1)
                initial_investment = st.number_input(
                    "Initial Investment (₹)", min_value=0, value=1000000, step=50000
                )
                target_amount = st.number_input(
                    "Target Amount (₹)", min_value=0, value=10000000, step=50000
                )
                if st.button("Get Recommendation"):
                    user_profile = {
                        'age': age,
                        'risk_score': risk_score,
                        'time_horizon': time_horizon,
                        'initial_investment': initial_investment,
                        'target_amount': target_amount
                    }
                    # Call the recommendation service
                    recommendation = api_client.get_recommendation(user_profile)
                    st.json(recommendation)
            else:
                # Disable inputs for chat
                st.write("Chat mode enabled. User profile inputs are disabled.")

        selected = option_menu(
            menu_title=None,
            options=["Chat", "Analytics", "Reports"],
            icons=["chat-dots", "graph-up", "file-text"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        if selected == "Chat" and mode == "Chat":
            chat_page = ChatPage(api_client, temperature, top_p)
            chat_page.initialize_session_state()
            chat_page.render()
        elif selected == "Chat" and mode == "Recommendation":
            st.write("Chat is disabled in Recommendation mode.")
        
        elif selected == "Analytics":
            st.title("Financial Analytics")
            
            if 'analysis_data' not in st.session_state:
                st.session_state.analysis_data = None
                
            uploaded_file = st.file_uploader("Upload financial data", type=['json'])
            if uploaded_file:
                analysis_data = json.load(uploaded_file)
                st.session_state.analysis_data = analysis_data
            
            if st.session_state.analysis_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Key Metrics")
                    create_metric_card(
                        "P/E Ratio",
                        "Value not provided",
                        st.session_state.analysis_data['ratios']['price_to_earnings']
                    )
                    create_metric_card(
                        "ROE",
                        "Value not provided",
                        st.session_state.analysis_data['ratios']['return_on_equity']
                    )
                
                with col2:
                    st.subheader("Financial Health")
                    create_metric_card(
                        "Debt to Equity",
                        "Value not provided",
                        st.session_state.analysis_data['financial_health']['debt_to_equity_ratio']
                    )
                    create_metric_card(
                        "Current Ratio",
                        "Value not provided",
                        st.session_state.analysis_data['financial_health']['current_ratio']
                    )
                
                st.subheader("Visual Analysis")
                tab1, tab2 = st.tabs(["Radar Analysis", "Trend Analysis"])
                
                with tab1:
                    radar_fig = create_radar_plot(st.session_state.analysis_data)
                    st.plotly_chart(radar_fig, use_container_width=True)
                
                with tab2:
                    trend_fig = create_trend_plot(st.session_state.analysis_data)
                    st.plotly_chart(trend_fig, use_container_width=True)
                
                if st.button("Download Full Report"):
                    figures = [radar_fig, trend_fig]
                    pdf_bytes = generate_pdf_report(
                        str(st.session_state.analysis_data),
                        figures
                    )
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name="financial_analysis_report.pdf",
                        mime="application/pdf"
                    )
            
        elif selected == "Reports":
            st.title("Reports")
            st.info("Reports feature coming soon...")
            
            st.subheader("Available Reports")
            reports = [
                "Market Overview",
                "Company Performance Analysis",
                "Sector Analysis",
                "Risk Assessment"
            ]
            
            for report in reports:
                with st.expander(report):
                    st.write("This report will be available in the next update.")
                    st.button(f"Generate {report}", key=report, disabled=True)
    elif authentication_status == False:
        st.error("Invalid username or password.")
    else:
        st.warning("Please login to access the dashboard.")

if __name__ == "__main__":
    main()
