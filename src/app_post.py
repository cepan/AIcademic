import streamlit as st
# from pdf_extraction_chatbot import pdf_extraction

# import chunk_vector
import embedding_post
import response_post

DATABASE_URI = 'mysql+mysqlconnector://root:55af5587f@localhost/dsci553'

st.title('My PDF Chatbot')

st.sidebar.header("Upload PDF")
# uploaded files should be in current directory
uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files", accept_multiple_files=True, type='pdf')


# for piazza posts
# text_ls = embedding_post.chunking(DATABASE_URI)
# path = "chroma_embedding_hugging_face"
# embedding.storing('posts', text_ls, path)

# Chat window
st.header("Chat with the bot")
user_input = st.text_input("Ask any question for course DSCI553:")
if user_input:
    response_text = response_post.generate_response(user_input)

    # response_text = "Response to your question: " + user_input
    st.text_area("Response", value=response_text,
                 height=300, max_chars=None, key=None)
