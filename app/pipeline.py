from app.extractor.extract_text import extract_texts_pdfs
from app.transformer.pdf_processor import create_filtered_pdf, get_metadata_pdf

import json

def pipeline():
    # text = extract_texts_pdfs(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\tecnologia_em_gastronomia.pdf", 1)
    # print(text)
    metadata = get_metadata_pdf(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\tecnologia_em_gastronomia.pdf", 2018)
    create_filtered_pdf(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\tecnologia_em_gastronomia.pdf", metadata)
    # json_final = exam_parser(cleaned_text)
    # print(json.dumps(json_final, ensure_ascii=False, indent=2))

    
pipeline()