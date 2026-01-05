from pathlib import Path
from app.core.settings import patterns
import fitz, re, os


QUESTAO_REGEX = re.compile(r"QUESTÃO\s+\d+", re.IGNORECASE)
ALTERNATIVA_E_REGEX = re.compile(r"^\s*[Ⓔ⊙●]?\s*E[\s\)]", re.MULTILINE)


def detect_questions(doc):
    questions = []
    for page_index, page in enumerate(doc):
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            if match := patterns.QUESTION.search(text):
                questions.append({
                    "page": page_index,
                    "y_start": y0,
                    "label": match.group(),
                    "y_end": None,
                    "page_end": None,
                    "skip": False
                })
    return questions


def find_end_questions(doc, question, max_pages=2):
    found_last_alternative = False
    acumulated_text = ""
    
    for offset in range(max_pages):
        page_index = question["page"] + offset
        page = doc[page_index]
        page_text = page.get_text()

        if offset <= 2:
            acumulated_text += page_text
        
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            if page_index == question["page"] and y0 < question["y_start"]:
                continue
            
            if found_last_alternative and patterns.QUESTION.search(text):
                return True
            
            if not found_last_alternative and patterns.LAST_ALTERNATIVE.search(text):
                found_last_alternative = True
            
            if found_last_alternative:
                question["page_end"] = page_index
                question["y_end"] = y1
                
                if text.strip().endswith('.'):
                    return True

    
    return True if found_last_alternative else False


def extract_questions(doc_origem, question, output_path):
    """Extrai uma questão e salva como PDF."""
    novo_doc = fitz.open()
    largura = doc_origem[question["page"]].rect.width
    
    # Calcular fragmentos
    fragmentos = []
    
    if question["page"] == question["page_end"]:
        # Questão em página única
        fragmentos.append({
            "page": question["page"],
            "clip": fitz.Rect(0, question["y_start"], largura, question["y_end"]),
            "altura": question["y_end"] - question["y_start"]
        })
    else:
        # Primeira página
        page = doc_origem[question["page"]]
        fragmentos.append({
            "page": question["page"],
            "clip": fitz.Rect(0, question["y_start"], largura, page.rect.height),
            "altura": page.rect.height - question["y_start"]
        })
        
        # Páginas intermediárias
        for p in range(question["page"] + 1, question["page_end"]):
            page = doc_origem[p]
            fragmentos.append({
                "page": p,
                "clip": page.rect,
                "altura": page.rect.height
            })
        
        # Última página
        fragmentos.append({
            "page": question["page_end"],
            "clip": fitz.Rect(0, 0, largura, question["y_end"]),
            "altura": question["y_end"]
        })
    
    # Criar página única
    altura_total = sum(f["altura"] for f in fragmentos)
    nova_pagina = novo_doc.new_page(width=largura, height=altura_total)
    
    # Posicionar fragmentos
    y_offset = 0
    for frag in fragmentos:
        destino = fitz.Rect(0, y_offset, largura, y_offset + frag["altura"])
        nova_pagina.show_pdf_page(destino, doc_origem, frag["page"], clip=frag["clip"])
        y_offset += frag["altura"]
    
    novo_doc.save(output_path, garbage=4, deflate=True)
    novo_doc.close()


def split_pdfs(pdf_path: str):
    doc = fitz.open(pdf_path)
    questions = detect_questions(doc)
    test_name = Path(pdf_path).stem

    for i, question in enumerate(questions):
        resultado = find_end_questions(doc, question)
        if resultado == False:
            question["skip"] = True

    for question in questions:
        if question["skip"] or question["y_end"] is None:
            continue
        
        question_number = question["label"].replace(" ", "_").lower()
        complete_name = test_name+"_"+question_number
        output_path = os.path.join("/data/tmp/splitted_pdf/", f"{complete_name}.pdf")
        
        extract_questions(doc, question, output_path)

    doc.close()