import streamlit as st
from openai import OpenAI
import os

import response_post
import pdf_embedding

st.title('AIcademic')

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
folder_path = os.path.join(parent_dir, 'uploaded_files')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

st.sidebar.header("Upload PDF")
uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files", accept_multiple_files=True, type='pdf')

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        #file = uploaded_file.read()
        # Include your processing logic here, e.g.:
        file_path = os.path.join(folder_path, uploaded_file.name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.read())
        pdf_embedding.pdf_extraction_embedding("../uploaded_files/" + uploaded_file.name)

            
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

    st.session_state['conversation_history'].insert(0,
                                                    (user_input, response_text, youtube_link))

# Display the latest conversation
if 'latest_question' in st.session_state and 'latest_response' in st.session_state:
    st.text_area(
        "You:", value=st.session_state['latest_question'], height=100, disabled=True)
    st.text_area(
        "AIcademic:", value=st.session_state['latest_response'], height=400, max_chars=None, disabled=True)

    # Embed the YouTube video if a link is available
    if 'latest_youtube_link' in st.session_state:
        st.video(st.session_state['latest_youtube_link'])


# Display existing conversation history
with st.container():
    for index, (question, response_text, youtube_link) in enumerate(st.session_state['conversation_history']):
        st.text_area("You:", value=question, height=100,
                     disabled=True, key=f"question_{index}")
        st.text_area("AIcademic:", value=response_text, height=300, max_chars=None,
                     disabled=True, key=f"response_text_{index}")
        st.text_area("AIcademic:", value=youtube_link, height=300, max_chars=None,
                     disabled=True, key=f"youtube_link_{index}")