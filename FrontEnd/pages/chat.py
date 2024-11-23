import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api import APIClient
import plotly.graph_objects as go
import json

class ChatPage:
    def __init__(self, api_client, temperature, top_p):
        self.api_client = api_client
        self.temperature = temperature
        self.top_p = top_p
        self.initialize_session_state()  # Ensure session state is initialized
        
    def initialize_session_state(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

# Assuming api_client is defined elsewhere and passed here
api_client = APIClient() # Replace with actual api_client initialization
chat_page = ChatPage(api_client, 0.5, 0.9)

st.title("AI Financial Advisor Chat")
st.markdown("### Chat")
prompt = st.text_area("Enter your question:", height=100)

if st.button("Submit"):
    if prompt:
        response = chat_page.api_client.chat_completion(prompt, chat_page.temperature, chat_page.top_p)
        response_text = response.get('response', 'No response available')
        st.session_state.chat_history.append({
            'sno': len(st.session_state.chat_history) + 1,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'prompt': prompt,
            'response': response_text
        })
        st.markdown("### Response :")
        st.write(response_text)
        visualization_prompt = f"Given the following response, give me  plots for appropriate data : {response_text}"
        visualization_response = chat_page.api_client.chat_completion(visualization_prompt, chat_page.temperature, chat_page.top_p)
        visualization_suggestion = visualization_response.get('response', 'No suggestion available')

        st.write(visualization_suggestion)
        
with st.expander("Chat History", expanded=True):
    if st.session_state.chat_history:
        df = pd.DataFrame(st.session_state.chat_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No chat history available.")
