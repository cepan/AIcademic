import openai
import chromadb
from chromadb.utils import embedding_functions
import chromadb.utils.embedding_functions as embedding_functions
import PyPDF2
from io import BytesIO
#from response_post import generate_response

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
print('Book PDFS')
for i in range(1, 14):
    text = pdf_extraction('../data/pdfs/book_pdfs/ch' + str(i) + '.pdf')
    entire_txt['book_ch_' + str(i)] = text

#PDF Slides
print('Slides 1')
for i in [1, 2, 3, 6, 7, 8, 11]:
    if i < 10:
        text = pdf_extraction('../data/pdfs/pdf_slides/ch0' + str(i) + '.pdf')
    else:
        text = pdf_extraction('../data/pdfs/pdf_slides/ch' + str(i) + '.pdf')
        
    entire_txt['slides_ch_' + str(i)] = text

print('Slides 2')
for i in [4, 5, 9, 10, 12]:
    if i < 10:
        text_1 = pdf_extraction('../data/pdfs/pdf_slides/ch0' + str(i) + '-1.pdf')
        text_2 = pdf_extraction('../data/pdfs/pdf_slides/ch0' + str(i) + '-2.pdf')
    else:
        text_1 = pdf_extraction('../data/pdfs/pdf_slides/ch' + str(i) + '-1.pdf')
        text_2 = pdf_extraction('../data/pdfs/pdf_slides/ch' + str(i) + '-2.pdf')
    
    entire_txt['slides_ch_' + str(i) + '_part1'] = text_1
    entire_txt['slides_ch_' + str(i) + '_part2'] = text_2


def storing(documents):
    huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
        api_key="hugging_face_api_key",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    openai.api_key = "open_ai_api_key"
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai.api_key,
        model_name="text-embedding-3-small"
    )
    chroma_client = chromadb.PersistentClient(path = "../chromadb/DSCI553")

    ids = ['id' + str(i) for i in range(len(documents))]

    # store embeddings to chroma
    collection = chroma_client.get_or_create_collection(
        name="embeddings_collection", embedding_function=huggingface_ef)
    collection.add(
        documents=documents,
        ids=ids)
    print("Successful")

documents = [entire_txt[key] for key in entire_txt.keys()]
storing(documents)

#while True:
#    user_question = input("What is your question?: ")
#    if user_question == "exit":
#        exit()
#    else:
#        answer = generate_response(user_question)
#        print(answer)