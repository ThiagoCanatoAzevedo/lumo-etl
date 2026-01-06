from app.extractor.extract_text import extract_texts_pdfs
import fitz, os, re
from pathlib import Path


def rename_pdfs(pdf_path:str):
    new_name = pdf_path.replace("_PV_", "")
    os.rename(pdf_path, new_name)
    

def get_metadata_pdf(pdf_path: str):
    extracted_text = extract_texts_pdfs(pdf_path, 1)
    
    def return_year_exam(extracted_text: str):
        return re.search(r"\b\d{4}\b", extracted_text).group()    
    
    def return_course_exam(extracted_text: str):    
        ignore = {'INSTRUÇÕES', 'ENADE', 'EXAME NACIONAL', 'MINISTÉRIO', 'NOVEMBRO', 
                'OUTUBRO', 'DEZEMBRO', 'VALIDINEP', 'LEIA COM ATENÇÃO'}

        return next((l for l in map(str.strip, extracted_text.split('\n')) 
            if l and l.isupper() and any(len(w) >= 4 for w in l.split()) 
            and not any(i in l for i in ignore)), None)
    
    def return_amount_pages(pdf_path: str) -> int:
        with fitz.open(pdf_path) as doc:
            return len(doc)
            
    return {'year_exam': return_year_exam(extracted_text), 'course_exam':return_course_exam(extracted_text), 'amount_pages': return_amount_pages(pdf_path)}

    
def clean_raw_text_pdfs(raw_text:str):
    """
    - remover textos estranho - VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDIN3P2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023VALIDINEP2023
    - remover textos
    """
    
    
    return raw_text