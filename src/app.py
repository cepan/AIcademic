import streamlit as st
from openai import OpenAI
import openai
import chromadb
from chromadb.utils import embedding_functions
import os


#  TO BE CHANGED LATER
os.environ["OPENAI_API_KEY"] = "you-openapi-key"
if os.getenv("OPENAI_API_KEY") is not None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    print("OPENAI_API_KEY environment variable not found")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get('OPENAI_API_KEY'),
    model_name="text-embedding-3-small"
)
# TO BE CHANGED LATER


DATABASE_URI = 'mysql+mysqlconnector://root:130136569shawN??0716@localhost/cook'

st.title('AIcademic')

st.sidebar.header("Upload PDF")
# uploaded files should be in current directory
uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files", accept_multiple_files=True, type='pdf')

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Existing processing logic here
        file = uploaded_file.read()
        # pdf_extraction(file, DATABASE_URI)
        # text_ls = chunk_vector.chunking(DATABASE_URI)
        path = "chroma_embedding"
        # chunk_vector.storing(uploaded_file.name, text_ls, path)

# Chat window for new questions
# st.header("Chat with the bot")
user_input = st.text_input("Questions")
client = OpenAI()

if user_input:

    # response_text = response.generate_response(user_input)
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=400,
        messages=[
            {"role": "user", "content": user_input}
        ])
    answer = response.choices[0].message.content

    st.session_state['conversation_history'].insert(0,
                                                    (user_input, answer))


# Display existing conversation history
with st.container():
    for index, (question, answer) in enumerate(st.session_state['conversation_history']):
        st.text_area("You:", value=question, height=100,
                     disabled=True, key=f"question_{index}")
        st.text_area("AIcademic:", value=answer, height=300, max_chars=None,
                     disabled=True, key=f"answer_{index}")
