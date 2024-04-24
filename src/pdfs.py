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
def pdf_extraction(file):
    text_pdf = ""
    with open(file, 'rb') as f:  # Open the file in binary mode
        stream_data = BytesIO(f.read())  # Read the content of the file and pass it to BytesIO
         
    pdfReader = PyPDF2.PdfReader(stream_data)

    for page in range(len(pdfReader.pages)):  # loop through pages
        pageObj = pdfReader.pages[page]
        text = pageObj.extract_text()
        text_pdf += text
    return text_pdf

entire_txt = {} #separate text into chapters by book/slides

#Book PDFS
for i in range(1, 14):
    text = pdf_extraction('../data/pdfs/book_pdfs/ch' + str(i) + '.pdf')
    entire_txt['book_ch_' + str(i)] = text

#PDF Slides
for i in [1, 2, 3, 6, 7, 8, 11]:
    if i < 10:
        text = pdf_extraction('../data/pdfs/pdf_slides/ch0' + str(i) + '.pdf')
    else:
        text = pdf_extraction('../data/pdfs/pdf_slides/ch' + str(i) + '.pdf')
        
    entire_txt['slides_ch_' + str(i)] = text

for i in [4, 5, 9, 10, 12]:
    if i < 10:
        text_1 = pdf_extraction('../data/pdfs/pdf_slides/ch0' + str(i) + '-1.pdf')
        text_2 = pdf_extraction('../data/pdfs/pdf_slides/ch0' + str(i) + '-2.pdf')
    else:
        text_1 = pdf_extraction('../data/pdfs/pdf_slides/ch' + str(i) + '-1.pdf')
        text_2 = pdf_extraction('../data/pdfs/pdf_slides/ch' + str(i) + '-2.pdf')
    
    entire_txt['slides_ch_' + str(i) + '_part1'] = text_1
    entire_txt['slides_ch_' + str(i) + '_part2'] = text_2

def storing(documents_dic):
    os.environ["OPENAI_API_KEY"] = "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"
    if os.getenv("OPENAI_API_KEY") is not None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("OPENAI_API_KEY environment variable not found")
    openai_ef = OpenCLIPEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path = "../chromadb/DSCI553")

    # store embeddings to chroma
    collection = chroma_client.get_or_create_collection(
        name="openclip", embedding_function=openai_ef)

    ids_embedded = set()
    for material in documents_dic:
        chunks = []
        text = documents_dic[material]
        for i in range(0, len(text), 2000):
            chunk =  text[i: i + 2000]
            chunks.append(chunk)

        for i in range(len(chunks)):
            id = material + str(i)
            if id not in ids_embedded: #not a duplicate id
                collection.add(documents = [chunks[i]], ids = [id])
                ids_embedded.add(id)

storing(entire_txt)