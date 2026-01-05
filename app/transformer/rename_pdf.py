import os


def rename_pdfs(pdf_path:str):
    new_name = pdf_path.replace("_PV_", "")
    os.rename(pdf_path, new_name)