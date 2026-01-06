from pathlib import Path
from app.core.settings import patterns
import fitz, os, re


def detect_questions(doc):
    questions = []
    for page_index, page in enumerate(doc):
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            if match := re.compile(patterns.FIND_QUESTION, re.IGNORECASE).search(text):
                questions.append({
                    "page": page_index, "y_start": y0, "label": match.group(),
                    "y_end": None, "page_end": None, "skip": False
                })
    return questions


def find_end_questions(doc, question, max_pages=2):
    found_last_alternative = False
    
    for offset in range(max_pages):
        page_index = question["page"] + offset
        page = doc[page_index]
        
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            if page_index == question["page"] and y0 < question["y_start"]:
                continue
            
            if found_last_alternative and re.compile(patterns.FIND_QUESTION, re.IGNORECASE).search(text):
                return True
            
            if re.compile(patterns.FIND_LAST_ALTERNATIVE, re.MULTILINE).search(text):
                found_last_alternative = True
                question["page_end"] = page_index
                question["y_end"] = y1
                
                if text.strip().endswith('.'):
                    return True
    
    return found_last_alternative


def extract_questions(source_doc, question, output_path):
    new_doc = fitz.open()
    width = source_doc[question["page"]].rect.width
    fragments = []
    
    if question["page"] == question["page_end"]:
        page = source_doc[question["page"]]
        fragments.append((question["page"], 
                          fitz.Rect(0, question["y_start"], width, question["y_end"]),
                          question["y_end"] - question["y_start"]))
    else:
        page = source_doc[question["page"]]
        fragments.append((question["page"],
                          fitz.Rect(0, question["y_start"], width, page.rect.height),
                          page.rect.height - question["y_start"]))
        
        for p in range(question["page"] + 1, question["page_end"]):
            page = source_doc[p]
            fragments.append((p, page.rect, page.rect.height))
        
        fragments.append((question["page_end"],
                          fitz.Rect(0, 0, width, question["y_end"]),
                          question["y_end"]))
    
    total_height = sum(height for _, _, height in fragments)
    new_page = new_doc.new_page(width=width, height=total_height)
    
    y_offset = 0
    for page_num, clip, height in fragments:
        dest = fitz.Rect(0, y_offset, width, y_offset + height)
        new_page.show_pdf_page(dest, source_doc, page_num, clip=clip)
        y_offset += height
    
    new_doc.save(output_path, garbage=4, deflate=True)
    new_doc.close()


def split_pdfs(pdf_path: str):
    doc = fitz.open(pdf_path)
    questions = detect_questions(doc)
    test_name = Path(pdf_path).stem

    for question in questions:
        if not find_end_questions(doc, question):
            question["skip"] = True

    for question in questions:
        if not question["skip"] and question["y_end"]:
            question_number = question["label"].replace(" ", "_").lower()
            output_path = os.path.join("/data/tmp/splitted_pdf/", 
                                      f"{test_name}_{question_number}.pdf")
            extract_questions(doc, question, output_path)

    doc.close()