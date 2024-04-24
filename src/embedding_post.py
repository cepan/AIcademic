from langchain_text_splitters import CharacterTextSplitter
from sqlalchemy import create_engine
import pandas as pd
import openai
import os
import chromadb
from chromadb.utils import embedding_functions
import chromadb.utils.embedding_functions as embedding_functions


def chunking(DATABASE_URI):
    engine = create_engine(DATABASE_URI)
    query = f"SELECT * FROM posts"
    df = pd.read_sql(query, engine)
    text_splitter = CharacterTextSplitter(
        separator='\n', chunk_size=1500, chunk_overlap=0)
    df['Combined'] = df.apply(lambda row: row['Question'] if row['Follow_Up'] is None else row['Question'] + ' ' + row['Follow_Up'], axis=1)
    question = ''.join([''.join(p) for p in df["Combined"]])
    text_ls = text_splitter.split_text(question)
    return text_ls


def storing(fn, text_ls, path):
    huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
        api_key="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",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    openai.api_key = "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"
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai.api_key,
        model_name="text-embedding-3-small"
    )
    chroma_client = chromadb.PersistentClient(path=path)

    # create embeddings
    embedding_ls = []
    id_ls = [fn+str(i) for i in range(len(text_ls))]

    # store embeddings to chroma

    collection = chroma_client.get_or_create_collection(
        name="embeddings_collection", embedding_function=huggingface_ef)
    if '' in text_ls:
        print("empty string")

    collection.add(
        documents=text_ls,
        ids=id_ls)

    print("Successfully stored chunks and embeddings to chroma, chroma did not embed the documents")

