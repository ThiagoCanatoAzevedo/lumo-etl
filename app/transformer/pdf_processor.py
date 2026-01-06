from app.extractor.extract_text import extract_texts_pdfs
from app.core.settings import patterns, settings
from pathlib import Path 
import fitz, re
    

def get_metadata_pdf(pdf_path: str, year_exam:int):
    extracted_text = extract_texts_pdfs(pdf_path, 1)
    
    def return_course_exam(extracted_text: str):    
        ignore = {'INSTRUÇÕES', 'ENADE', 'EXAME NACIONAL', 'MINISTÉRIO', 'NOVEMBRO', 
                'OUTUBRO', 'DEZEMBRO', 'VALIDINEP', 'LEIA COM ATENÇÃO', 'SINAES'}

        return next((l for l in map(str.strip, extracted_text.split('\n')) 
            if l and l.isupper() and any(len(w) >= 4 for w in l.split()) 
            and not any(i in l for i in ignore)), None).lower()
                
    
    def return_amount_pages(pdf_path: str) -> int:
        with fitz.open(pdf_path) as doc:
            return len(doc)
            
    return {'year_exam': year_exam, 'course_exam': return_course_exam(extracted_text), 'amount_pages': return_amount_pages(pdf_path)}



def create_filtered_pdf(pdf_path: str, metadata):
    amount_pages = metadata.get("amount_pages")
    year_exam = metadata.get("year_exam")
    couse_exam = metadata.get("course_exam")
    
    doc = fitz.open(pdf_path)
    new_doc = fitz.open()

    for i in range(amount_pages):
        extracted_text = extract_texts_pdfs(pdf_path, i+1)
        if (re.search(patterns.FIND_ALTERNATIVES, extracted_text)and not re.search(patterns.FIND_TRASH_TEXT, extracted_text)):
            new_doc.insert_pdf(doc, from_page=i, to_page=i)

    new_doc.save(Path(f"{settings.TMP_DIR}/{year_exam}_{couse_exam}.pdf"))
    new_doc.close()
    doc.close()