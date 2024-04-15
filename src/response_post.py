import openai
import chromadb
from chromadb.utils import embedding_functions
import os
from openai import OpenAI


def generate_response(query):
    # hugging face embedding function
    huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
        api_key="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",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    # openai ebedding function
    # set apikey
    os.environ["OPENAI_API_KEY"] = "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"
    if os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("OPENAI_API_KEY environment variable not found")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ.get('OPENAI_API_KEY'),
        model_name="text-embedding-3-small"
    )

    # initializing openAI
    client = OpenAI()
    # getting chroma_db
    chroma_client = chromadb.PersistentClient(
        path="chroma_embedding_hugging_face")
    # accessing collection
    collection = chroma_client.get_collection(
        "embeddings_collection", embedding_function=huggingface_ef)
    # query based on collection
    results = collection.query(
        query_texts=query, n_results=5, include=['documents'])

    relevant = results["documents"][0]
    context = "\n\n".join(relevant) + "\n\n" + query

    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=400,
        messages=[
            {"role": "system", "content": "How may I help you with ADS Cookbook?"},
            {"role": "user", "content": context}
        ])
    return response.choices[0].message.content

