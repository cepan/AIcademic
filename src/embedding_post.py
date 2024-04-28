from langchain_text_splitters import CharacterTextSplitter
from sqlalchemy import create_engine
import pandas as pd
import openai
import os
import chromadb
from chromadb.utils import embedding_functions
import chromadb.utils.embedding_functions as embedding_functions
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
def create_posts_db():
    DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/dsci553'

    os.environ["OPENAI_API_KEY"] = "api_key"
    if os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("OPENAI_API_KEY environment variable not found")

    engine = create_engine(DATABASE_URI)
    query = f"SELECT * FROM posts"
    df = pd.read_sql(query, engine)
    df.to_csv('piazza.csv')
    text_splitter = CharacterTextSplitter(
        separator='\n', chunk_size=1500, chunk_overlap=0)
    df['Combined'] = df.apply(lambda row: row['Question'] if row['Follow_Up'] is None else row['Question'] + ' ' + row['Follow_Up'], axis=1)
    question = ''.join([''.join(p) for p in df["Combined"]])
    text_ls = text_splitter.split_text(question)


    chroma_client = chromadb.PersistentClient(path="DSCI553")
    openai_ef = OpenCLIPEmbeddingFunction()
    # create embeddings
    id_ls = ['posts'+str(i) for i in range(len(text_ls))]
    # store embeddings to chroma
    collection = chroma_client.get_or_create_collection(
        name="openclip", embedding_function=openai_ef)
    if '' in text_ls:
        print("empty string")

    collection.add(
        documents=text_ls,
        ids=id_ls)

    print("Successfully stored chunks and embeddings to chroma, chroma did not embed the documents")
