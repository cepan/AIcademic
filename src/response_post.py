import openai
import chromadb
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
import os
from openai import OpenAI
import json


def generate_response(query):
    # openai ebedding function
    # set api
    os.environ["OPENAI_API_KEY"] = "openai_api_key"
    if os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("OPENAI_API_KEY environment variable not found")

    openai_ef = OpenCLIPEmbeddingFunction(
        # api_key=os.environ.get('OPENAI_API_KEY')
    )

    # initializing openAI
    client = OpenAI()
    # getting chroma_db
    chroma_client = chromadb.PersistentClient(
        path="../chromadb/DSCI553")

    collection = chroma_client.get_collection(
        name="openclip", embedding_function=openai_ef)

    results = collection.query(
        query_texts=query, n_results=1, include=['documents', 'metadatas', 'uris'])

    context = results["documents"][0][0] + \
        "\n\n" + query

    response_video_url = results["metadatas"][0][0]['youtube_link']

    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=400,
        messages=[
            {"role": "system", "content": "respond at the end with the provided youtube link for in-dpeth explanation"},
            {"role": "user", "content": context}
        ])

    return response.choices[0].message.content, response_video_url
