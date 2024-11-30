import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api import APIClient
from fpdf import FPDF
import io

class ChatPage:
    def __init__(self, api_client, temperature, top_p):
        self.api_client = api_client
        self.temperature = temperature
        self.top_p = top_p

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
        st.title("AI Financial Advisor Chat")

        self.initialize_session_state()

        st.markdown("### Chat")
        prompt = st.text_area("Enter your question:", height=100)

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
