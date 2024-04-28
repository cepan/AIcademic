import pdf_embedding

#Book PDFS
for i in range(1, 14):
    text = pdf_embedding.pdf_extraction_embedding('../data/pdfs/book_pdfs/ch' + str(i) + '.pdf')

#PDF Slides
for i in [1, 2, 3, 6, 7, 8, 11]:
    if i < 10:
        text = pdf_embedding.pdf_extraction_embedding('../data/pdfs/pdf_slides/ch0' + str(i) + '.pdf')
    else:
        text = pdf_embedding.pdf_extraction_embedding('../data/pdfs/pdf_slides/ch' + str(i) + '.pdf')

for i in [4, 5, 9, 10, 12]:
    if i < 10:
        text_1 = pdf_embedding.pdf_extraction_embedding('../data/pdfs/pdf_slides/ch0' + str(i) + '-1.pdf')
        text_2 = pdf_embedding.pdf_extraction_embedding('../data/pdfs/pdf_slides/ch0' + str(i) + '-2.pdf')
    else:
        text_1 = pdf_embedding.pdf_extraction_embedding('../data/pdfs/pdf_slides/ch' + str(i) + '-1.pdf')
        text_2 = pdf_embedding.pdf_extraction_embedding('../data/pdfs/pdf_slides/ch' + str(i) + '-2.pdf')