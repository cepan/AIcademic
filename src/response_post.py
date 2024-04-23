import openai
import chromadb
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
import os
from openai import OpenAI


def generate_response(query):
    # # hugging face embedding function
    # huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    #     api_key="your-hugging_faceapi",
    #     model_name="sentence-transformers/all-MiniLM-L6-v2"
    # )
    # openai ebedding function
    # set api
    os.environ["OPENAI_API_KEY"] = ""
    if os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("OPENAI_API_KEY environment variable not found")

    openai_ef = OpenCLIPEmbeddingFunction(
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    # initializing openAI
    client = OpenAI()
    # getting chroma_db
    chroma_client = chromadb.PersistentClient(
        path="../chromadb/DSCI553")
    # accessing collection
    # print(chroma_client.list_collections())
    collection = chroma_client.get_collection(
        "embeddings_collection", embedding_function=openai_ef)
    # query based on collection
    # print(query)
    results = collection.query(
        query_texts=query, n_results=5, include=['documents'])

    relevant = results["documents"][0]
    context = "\n\n".join(relevant) + "\n\n" + query

    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=400,
        messages=[
            {"role": "system", "content": "How may I help you?"},
            {"role": "user", "content": context}
        ])
    return response.choices[0].message.content
