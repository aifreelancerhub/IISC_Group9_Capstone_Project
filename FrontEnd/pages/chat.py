import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api import APIClient
from fpdf import FPDF
from st_audiorec import st_audiorec
import requests
from datetime import datetime
import os

class ChatPage:
    def __init__(self, api_client, temperature, top_p):
        self.api_client = api_client
        self.temperature = temperature
        self.top_p = top_p
       
    default_questions = [
        "What are the best investment options for beginners?",
        "How can I save for retirement effectively?",
        "What is a good monthly budget plan?",
        "Should I invest in stocks or mutual funds?",
        "How can I improve my credit score?"
    ]

    def initialize_session_state(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'pdf_ready' not in st.session_state:
            st.session_state.pdf_ready = False
        if 'pdf_bytes' not in st.session_state:
            st.session_state.pdf_bytes = None

    def format_prompt(self, user_prompt):
        """Format the prompt to get detailed response"""
        template = f"""
        Analyze the following query and provide a detailed response with both numerical values and explanations:
        {user_prompt}
        """
        return template

    def generate_summary(self, response_text):
        """Generate a text summary from plain text response"""
        # Directly use the response text as the summary
        return response_text

    def generate_pdf_report(self, summary_text):
        """Generate PDF report from summary text"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Financial Analysis Report', ln=True, align='C')

        pdf.set_font('Arial', '', 12)
        pdf.ln(10)
        pdf.multi_cell(0, 10, summary_text)

        pdf_output = pdf.output(dest='S').encode('latin1')
        return pdf_output

    def render(self):
        self.initialize_session_state()
        transcribed_text=""
        st.markdown("### Chat with default questions")

        selected_question = st.selectbox(
        "Choose a question to ask:", self.default_questions, index=None
        )

        if selected_question:
            st.write(f"**You selected:** {selected_question}")
            response = self.api_client.chat_completion(selected_question, self.temperature, self.top_p)
            
            # Debugging: Print response type and content
            print("Response Type:", type(response))
            print("Response Content:", response)

            # If response is a string, convert it to a dictionary
            if isinstance(response, str):
                try:
                    temp = {}
                    temp["response"] = response  # Wrap the string response in a dictionary
                    response = temp
                except Exception as e:
                    st.error(f"Failed to process response: {e}")
                    return

            response_text = response.get('response', 'No response available.')


            # Save to session state
            st.session_state.chat_history.append({
                'sno': len(st.session_state.chat_history) + 1,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'prompt': selected_question,
                'response': response_text
            })

            # Display the response
            st.markdown("### Response:")
            st.write(response_text)


        st.write("OR")

        st.markdown("### Ask me a question! via speech or text")

        # Initialize history in session state
        if "history" not in st.session_state:
            st.session_state.history = []

        # Record Audio Section
        st.markdown("### Record Prompt")
        audio_data = st_audiorec()

        if audio_data is not None:
            # Save recorded audio to a temporary file
            temp_audio_path = f"MyAudios/audio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"
            os.makedirs("MyAudios", exist_ok=True)  # Ensure directory exists
            with open(temp_audio_path, "wb") as f:
                f.write(audio_data)

            # Send audio file to backend for transcription
            with open(temp_audio_path, "rb") as audio:
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/api/v1/transcribe/",  # FastAPI endpoint
                        files={"file": audio}
                    )
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to backend: {e}")
                    os.remove(temp_audio_path)
                    st.stop()

            # Check response from the backend
            if response.status_code == 200:
                transcription_data = response.json()
                transcribed_text = transcription_data.get("transcription", "No transcription available")

                # Display result in a text area
                # st.text_area("Speech to Text", value=transcribed_text, height=150)

                # Update history in session state
                st.session_state.history.append(
                    {"filename": os.path.basename(temp_audio_path), "transcription": transcribed_text}
                )
            else:
                st.error(f"Failed to transcribe audio: {response.json().get('detail', 'Unknown error')}")

            # Remove temporary file
            os.remove(temp_audio_path)
        '''
        # Show transcription history in an expander
        with st.expander("Transcription History"):
            if st.session_state.history:
                for entry in st.session_state.history:
                    st.write(f"**File Name:** {entry['filename']}")
                    st.write(f"**Transcription:** {entry['transcription']}")
                    st.write("---")
            else:
                st.write("No transcriptions yet.")'''

        # prompt = st.text_area("Enter your question:", height=100)
        prompt = st.text_area("Enter your question:",  value=transcribed_text, height=100)

        submit = st.button("Submit")

        # Disable download button initially
        if not st.session_state.pdf_ready:
            download_disabled = True
        else:
            download_disabled = False

        if submit:
            if prompt:
                st.session_state.pdf_ready = False  # Disable download button
                st.session_state.pdf_bytes = None
                # Placeholder for processing
                with st.spinner('Generating report...'):
                    formatted_prompt = self.format_prompt(prompt)
                    response_text = self.api_client.chat_completion(formatted_prompt, self.temperature, self.top_p)
                    # print("Check1",response_text)
                    # Directly use the plain text response
                    summary_text = self.generate_summary(response_text)
                    st.text_area("Summary", summary_text, height=300)
                    # Generate PDF report
                    pdf_bytes = self.generate_pdf_report(summary_text)
                    st.session_state.pdf_bytes = pdf_bytes
                    st.session_state.pdf_ready = True
                    st.success("Report is ready for download.")

                    st.session_state.chat_history.append({
                        'sno': len(st.session_state.chat_history) + 1,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'prompt': prompt,
                        'response': response_text
                    })
            else:
                st.warning("Please enter a question.")
        else:
            pass  # Do nothing if submit is not clicked

        # Download button
        if st.session_state.pdf_ready:
            st.download_button(
                label="Download Report",
                data=st.session_state.pdf_bytes,
                file_name='financial_analysis_report.pdf',
                mime='application/pdf'
            )
        else:
            st.button(
                label="Download Report",
                disabled=True
            )

        with st.expander("Chat History", expanded=True):
            if st.session_state.chat_history:
                df = pd.DataFrame(st.session_state.chat_history)
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No chat history available.")
