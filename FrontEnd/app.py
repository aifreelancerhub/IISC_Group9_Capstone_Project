import streamlit as st
from streamlit_option_menu import option_menu
# from utils.auth import Authentication
from utils.api import APIClient
from pages.chat import ChatPage
from pages.analytics import AnalyticsPage

st.set_page_config(
    page_title="Financial Advisor Dashboard",
    page_icon="💼",
    layout="wide"
)

def main():
    # auth = Authentication()
    # name, authentication_status, username = auth.authenticate()

    # if authentication_status:
    with st.sidebar:
        st.title("Configuration")
        temperature = st.slider("AI Temperature", 0.0, 1.0, 0.7, 0.1,
                             help="Controls randomness in AI responses")
        top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1,
                        help="Controls diversity of AI responses")
        # st.write(f"Welcome, {name}")
        # auth.logout()

    selected = option_menu(
        menu_title=None,
        options=["Chat", "Analytics", "Reports"],
        icons=["chat-dots", "graph-up", "file-text"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    api_client = APIClient()
    if selected == "Chat":
        chat_page = ChatPage(api_client, temperature, top_p)
        chat_page.initialize_session_state()
        chat_page.render(True)  # Pass True to bypass authentication
    elif selected == "Analytics":
        analytics_page = AnalyticsPage(api_client)
        analytics_page.render(True)  # Pass True to bypass authentication
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

if __name__ == "__main__":
    main()
