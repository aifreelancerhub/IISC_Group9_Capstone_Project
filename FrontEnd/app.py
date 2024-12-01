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
import requests

st.set_page_config(
    page_title="Nifty20 Advisor Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"

)

# Custom CSS for fixed header and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} 
        header {visibility: hidden;}  
        footer {visibility: hidden;} 
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: #f0f2f6; /* Header background color */
            padding: 10px 10px 10px 35px; /* top right bottom left for the header */
            text-align: Center; /* Center align text */
            z-index: 1000; /* Ensure it's on top of other elements */
            font-size: 24px; /* Font size for the header */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5); /* Add a shadow for visibility */
        }
        .logo {
            position: absolute; /* Positioning it in the header */
            top: 15px; /* Adjust as necessary */
            right: 45px; /* Adjust as necessary */
            height: 50px; /* Set the height of the logo */
        }
        .report-title {
            font-size: 28px; /* Size for Report.AI */
            color: #31333F; /* Color for emphasis */
        }
        @media (min-width: 576px) {
            .st-emotion-cache-1jicfl2 {
                padding-left: 2rem !important; /* Override left padding */
                padding-right: 2rem !important; /* Override right padding */
            }
        }
        .st-emotion-cache-hzo1qh {
            position: fixed;
            left: 1.5rem;
            top: 0rem;
            z-index: 999990;
            display: flex;
            -moz-box-pack: center;
            justify-content: center;
            -moz-box-align: center;
            align-items: center;
            }
        .st-emotion-cache-j6t2ck {
            margin: 0.25rem 0.5rem 0.25rem 0px;
            z-index: 999990;
            object-fit: contain;
            height: 4.5rem;
            }
        .fixed-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            font-size: 12px; /* Font size for the footer */
            font-weight: bold; /* Bold style */
            background-color: #f0f2f6; /* Footer background color */
            padding: 10px; /* Padding for the footer */
            text-align: center; /* Center align text */
            z-index: 1000; /* Ensure it's on top of other elements */
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.5); /* Add shadow for visibility (upwards) */
        }
    </style>
""", unsafe_allow_html=True)
# Inject CSS to hide the sidebar
st.markdown("""
    <style>
        .css-1d391kg {display: none;}  /* Hide sidebar completely */
    </style>
""", unsafe_allow_html=True)
# Header with different text sizes
st.markdown('''
    <div class="fixed-header">
        <h3 class="report-title">💼 Nifty20 Advisor – Your AI-Driven Financial Mentor</h3>
    </div>
''', unsafe_allow_html=True)

logo_image_path="images/IISc_Seal_Master_logo.png"
# Use st.logo to display the logo
st.logo(logo_image_path, size="large", link=None, icon_image=logo_image_path)

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

# Function to fetch news and display it in a table
def fetch_and_display_news():
    # Make the API call to your FastAPI endpoint
    response = requests.get("http://localhost:8000/api/v1/news-summary")  # Adjust URL as needed
    if response.status_code == 200:
        data = response.json()['data']  # Assuming 'data' contains the list of news items
        # Convert the JSON response into a DataFrame
        news_df = pd.DataFrame(data)
        
        # Display the DataFrame as a table in Streamlit
        # st.write("### Live News Recommendation")
        # st.write(news_df[['company', 'datetime', 'news_content', 'summary']])
        
        # Optionally, you can add formatting or an interactive table here
        st.dataframe(news_df[['company', 'datetime','news_content', 'summary']])
    else:
        st.error("Failed to fetch news data.")

def main():
    auth = Authentication()
    name, authentication_status, username = auth.authenticate()
    if authentication_status:
        col1,col3, col2 = st.columns([0.7,0.1,3.2])  # 1:3 ratio for sidebar-like content and main content

        with col1:
            st.subheader(f"Welcome !, :red[_{name}_]")
            auth.logout()
            st.markdown("#### Configuration")

            # Initialize temperature and top_p
            temperature = 0.7
            top_p = 0.9
            # Enable inputs for recommendation
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
            top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1)

            # Radio buttons for mode selection
            mode = st.radio("Select Mode", ("Recommendation", "Chat Advisory"))
            


            api_client = APIClient()  # Initialize APIClient here
            
            if mode == "Recommendation":
                st.markdown("#### User Profile")
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
                st.write("Chat Advisory mode enabled. User profile inputs are disabled.")
        with col2:
            selected = option_menu(
                menu_title="Nifty20 NSE Companies",
                options=["Financial Advisory", "Live News Recommendation"],
                icons=["chat-dots", "newspaper"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal"
            )


            if selected == "Financial Advisory" and mode == "Chat Advisory":
                chat_page = ChatPage(api_client, temperature, top_p)
                chat_page.initialize_session_state()
                chat_page.render()
            elif selected == "Financial Advisory" and mode == "Recommendation":
                st.write("Chat is disabled in Recommendation mode.")
            
            elif selected == "Live News Recommendation":
                st.title("Live News Recommendation")

                # Button to fetch and display the live news
                if st.button('Extract Live News for Top 20 Nifty Companies'):
                    fetch_and_display_news()  # Function to fetch and display news
        
    elif authentication_status == False:
        st.error("Invalid username or password.")
    else:
        st.warning("Please login to access the dashboard.")
# Footer
st.markdown('<div class="fixed-footer"> Nifty20 Advisor AI Agent, © 2024 | Built by 💡 Group9 , IISC & Talentsprint GenAI Hub 💡</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
