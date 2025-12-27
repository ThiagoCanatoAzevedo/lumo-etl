import os
import sys
from app.state import etl_stop_event
from app.crawler.discover import discover_pdfs
from app.crawler.filter import filter_downloadable_pdfs
from app.crawler.downloader import download_pdfs

from app.extractor.classifier import classify_pdfs
from app.extractor.reader import read_pdfs
from app.extractor.test_parser import test_parser
from app.extractor.solution_parser import solution_parser


def process_test(text: str, meta: dict):
    try:
        return {
            "metadata": meta,
            "questoes": test_parser(text),
            "error": None
        }
    except Exception as e:
        return {
            "metadata": meta,
            "questoes": [],
            "error": str(e)
        }


def process_solution(text: str, meta: dict):
    try:
        return {
            "metadata": meta,
            "respostas": solution_parser(text),
            "error": None
        }
    except Exception as e:
        return {
            "metadata": meta,
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

    for item in discovered:
        if etl_stop_event.is_set():
            break

        # ignorar PDFs que não queremos
        if not filter_downloadable_pdfs(item):
            skipped += 1
            continue

        pdf_path = None

        try:
            pdf_path = download_pdfs(item["url"])
            text = read_pdfs(pdf_path)

            tipo = classify_pdfs(item["filename"])

            if tipo == "prova":
                provas.append(process_test(text, item))

            elif tipo == "gabarito":
                gabaritos.append(process_solution(text, item))

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
                except:
                    pass

    return {
        "year": year,
        "processed": processed,
        "skipped": skipped,
        "errors": errors,
        "stopped": etl_stop_event.is_set(),
        "total_questoes": sum(len(p["questoes"]) for p in provas),
        "total_respostas": sum(len(g["respostas"]) for g in gabaritos),
        "provas": provas,
        "gabaritos": gabaritos
    }


def validate_results(result: dict) -> dict:
    def categorize(items, key):
        ok = sum(1 for i in items if i.get(key))
        empty = sum(1 for i in items if not i.get(key) and not i.get("error"))
        err = sum(1 for i in items if i.get("error"))
        return ok, empty, err

    provas_ok, provas_vazias, provas_err = categorize(result["provas"], "questoes")
    gab_ok, gab_vazios, gab_err = categorize(result["gabaritos"], "respostas")

    return {
        "provas_ok": provas_ok,
        "provas_vazias": provas_vazias,
        "provas_com_erro": provas_err,
        "gabaritos_ok": gab_ok,
        "gabaritos_vazios": gab_vazios,
        "gabaritos_com_erro": gab_err,
    }


if __name__ == "__main__":
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2023
    result = run_pipeline(year)
    print(validate_results(result))
