import openai
import os
import chromadb
from chromadb.utils import embedding_functions
import chromadb.utils.embedding_functions
import PyPDF2
from io import BytesIO
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction

# Helper Functions
#-------------------------------------------------------------------------------
#Extract PDF information
def pdf_extraction_embedding(file):
    text_pdf = ""
    with open(file, 'rb') as f:  # Open the file in binary mode
        stream_data = BytesIO(f.read())  # Read the content of the file and pass it to BytesIO
         
    pdfReader = PyPDF2.PdfReader(stream_data)

    for page in range(len(pdfReader.pages)):  # loop through pages
        pageObj = pdfReader.pages[page]
        text = pageObj.extract_text()
        text_pdf += text

    os.environ["OPENAI_API_KEY"] = "openai_api_key"
    if os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("OPENAI_API_KEY environment variable not found")
    openai_ef = OpenCLIPEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path = "../chromadb/DSCI553")

    # store embeddings to chroma
    collection = chroma_client.get_or_create_collection(
        name="openclip", embedding_function=openai_ef)

    chunks = []
    for i in range(0, len(text), 2000):
        chunk =  text[i: i + 2000]
        chunks.append(chunk)

    for i in range(len(chunks)):
        id = file + str(i)
        collection.add(documents=[chunks[i]], ids=[id])

#Book PDFS
for i in range(1, 14):
    text = pdf_extraction_embedding('../data/pdfs/book_pdfs/ch' + str(i) + '.pdf')

#PDF Slides
for i in [1, 2, 3, 6, 7, 8, 11]:
    if i < 10:
        text = pdf_extraction_embedding('../data/pdfs/pdf_slides/ch0' + str(i) + '.pdf')
    else:
        text = pdf_extraction_embedding('../data/pdfs/pdf_slides/ch' + str(i) + '.pdf')

for i in [4, 5, 9, 10, 12]:
    if i < 10:
        text_1 = pdf_extraction_embedding('../data/pdfs/pdf_slides/ch0' + str(i) + '-1.pdf')
        text_2 = pdf_extraction_embedding('../data/pdfs/pdf_slides/ch0' + str(i) + '-2.pdf')
    else:
        text_1 = pdf_extraction_embedding('../data/pdfs/pdf_slides/ch' + str(i) + '-1.pdf')
        text_2 = pdf_extraction_embedding('../data/pdfs/pdf_slides/ch' + str(i) + '-2.pdf')