from app.extractor.extract_text import extract_texts_pdfs
from app.transformer.pdf_processor import create_filtered_pdf, get_metadata_pdf
from app.parser.exam_parser import exam_parser
from app.transformer.text_processor import clean_raw_text_pdf

import json

def pipeline(pdf_path:str, year_exam:int):
    metadata = get_metadata_pdf(pdf_path, year_exam)
    filtered_pdf_path = create_filtered_pdf(pdf_path, metadata)
    raw_text = extract_texts_pdfs(filtered_pdf_path, 9)
    print("---------- raw text ----------")
    print(raw_text)
    print("---------- cleaned text ----------")
    cleaned_text = clean_raw_text_pdf(raw_text, metadata)
    print(cleaned_text)
    # json_final = exam_parser(cleaned_text)
    # print(json.dumps(json_final, ensure_ascii=False, indent=2))

    
pipeline(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\tecnologia_em_gastronomia.pdf", 2019)