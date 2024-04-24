import streamlit as st
from openai import OpenAI

import response_post

st.title('AIcademic')

st.sidebar.header("Upload PDF")
uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files", accept_multiple_files=True, type='pdf')

if uploaded_files:
    for uploaded_file in uploaded_files:
        file = uploaded_file.read()
        # Include your processing logic here, e.g.:
        # pdf_extraction(file, DATABASE_URI)
        # text_ls = chunk_vector.chunking(DATABASE_URI)
        # chunk_vector.storing(uploaded_file.name, text_ls, path)

# Chat window for new questions
user_input = st.text_input("Ask a question:")

if user_input:
    # Generate response using some backend logic or API
    response_text, youtube_link = response_post.generate_response(
        user_input)
    # Store the latest conversation and other elements only
    st.session_state['latest_question'] = user_input
    st.session_state['latest_response'] = response_text
    st.session_state['latest_youtube_link'] = youtube_link

# Display the latest conversation
if 'latest_question' in st.session_state and 'latest_response' in st.session_state:
    st.text_area(
        "You:", value=st.session_state['latest_question'], height=100, disabled=True)
    st.text_area(
        "AIcademic:", value=st.session_state['latest_response'], height=400, max_chars=None, disabled=True)

    # Embed the YouTube video if a link is available
    if 'latest_youtube_link' in st.session_state:
        st.video(st.session_state['latest_youtube_link'])
