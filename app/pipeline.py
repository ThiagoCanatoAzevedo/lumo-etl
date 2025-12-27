import os, sys
from app.state import etl_stop_event
from app.crawler.discover import discover_pdfs
from app.crawler.filter import filter_downloadable_pdfs
from app.crawler.downloader import download_pdfs

from app.extractor.classifier import classify_pdf
from app.extractor.reader import read_pdfs
from app.extractor.test_parser import test_parser
from app.extractor.solution_parser import solution_parser


def process_test(text: str, metadata: dict) -> dict:
    try:
        questoes = test_parser(text)        
        return {
            "metadata": metadata,
            "questoes": questoes
        }
    except Exception as e:
        return {
            "metadata": metadata,
            "questoes": [],
            "error": str(e)
        }


def process_solution(text: str, metadata: dict) -> dict:
    try:
        respostas = solution_parser(text)        
        return {
            "metadata": metadata,
            "respostas": respostas
        }
    except Exception as e:
        return {
            "metadata": metadata,
            "respostas": {},
            "error": str(e)
        }


def run_pipeline(year: int) -> dict:
    etl_stop_event.clear()
    discovered = discover_pdfs(year)
    
    provas = []
    gabaritos = []
    processed = 0
    skipped = 0
    errors = 0
        
    for idx, item in enumerate(discovered, 1):
        if etl_stop_event.is_set():
            break
                
        if not filter_downloadable_pdfs(item):
            skipped += 1
            continue
        
        pdf_path = None
        try:
            pdf_path = download_pdfs(item["url"])
            
            if etl_stop_event.is_set():
                break
            
            tipo = classify_pdf(item["filename"])
            text = read_pdfs(pdf_path)
            
            if tipo == "prova":
                resultado = process_test(text, item)
                provas.append(resultado)
                
            elif tipo == "gabarito":
                resultado = process_solution(text, item)
                gabaritos.append(resultado)
            
            else:
                skipped += 1
                continue
            
            processed += 1
            
        except Exception as e:
            errors += 1
        finally:
            if pdf_path and os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                except Exception as e:
                    print(e)
    
    total_questoes = sum(len(p.get('questoes', [])) for p in provas)
    total_respostas = sum(len(g.get('respostas', {})) for g in gabaritos)
    
    return {
        "year": year,
        "processed": processed,
        "stopped": etl_stop_event.is_set(),
        "skipped": skipped,
        "errors": errors,
        "total_questoes": total_questoes,
        "total_respostas": total_respostas,
        "provas": provas,
        "gabaritos": gabaritos
    }


def validate_results(result: dict) -> dict:
    validacao = {
        "provas_ok": 0,
        "provas_vazias": 0,
        "provas_com_erro": 0,
        "gabaritos_ok": 0,
        "gabaritos_vazios": 0,
        "gabaritos_com_erro": 0,
        "questoes_por_prova": []
    }
    
    for prova in result.get("provas", []):
        if prova.get("error"):
            validacao["provas_com_erro"] += 1
        elif not prova.get("questoes"):
            validacao["provas_vazias"] += 1
        else:
            validacao["provas_ok"] += 1
            validacao["questoes_por_prova"].append({
                "arquivo": prova["metadata"]["filename"],
                "questoes": len(prova["questoes"])
            })
    
    for gabarito in result.get("gabaritos", []):
        if gabarito.get("error"):
            validacao["gabaritos_com_erro"] += 1
        elif not gabarito.get("respostas"):
            validacao["gabaritos_vazios"] += 1
        else:
            validacao["gabaritos_ok"] += 1
    
    return validacao


if __name__ == "__main__":
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2023
    result = run_pipeline(year)
    validacao = validate_results(result)