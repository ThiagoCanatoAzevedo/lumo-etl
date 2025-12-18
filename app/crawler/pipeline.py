from app.state import etl_stop_event
from app.crawler.discover import discover_pdfs
from app.crawler.filter import filter_downloadable_pdfs
from app.crawler.downloader import download_pdfs
from app.extractor.cleaner import clean_pdf
import os


def run_pipeline(year: int) -> dict:
    etl_stop_event.clear()

    discovered = discover_pdfs(year)
    processed = 0

    for item in discovered:
        if etl_stop_event.is_set():
            break

        if not filter_downloadable_pdfs(item):
            continue

        pdf_path = download_pdfs(item["url"])

        try:
            if etl_stop_event.is_set():
                break

            clean_pdf(pdf_path, item)
            processed += 1
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    return {
        "year": year,
        "processed": processed,
        "stopped": etl_stop_event.is_set()
    }
