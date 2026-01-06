import os


def rename_pdfs(pdf_path:str):
    new_name = pdf_path.replace("_PV_", "")
    os.rename(pdf_path, new_name)
    
def clean_raw_text_pdfs(raw_text:str):
    return raw_text