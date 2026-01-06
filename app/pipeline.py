from app.extractor.extract_text import extract_texts_pdfs
from app.transformer.pdf_processor import clean_raw_text_pdfs
from app.parser.exam_parser import exam_parser

from app.transformer.pdf_processor import get_metadata_pdf

import json

def pipeline():
    # get_metadata_pdf(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\ARQUITETURA.pdf")
    raw_text = extract_texts_pdfs(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\2023_PV_agronomia.pdf", 1)
    cleaned_text = clean_raw_text_pdfs(raw_text)
    # print(cleaned_text)
    # json_final = exam_parser(cleaned_text)
    # print(json.dumps(json_final, ensure_ascii=False, indent=2))

    
pipeline()