from pathlib import Path
from app.core.settings import settings
import fitz, os


def extract_images_pdfs(pdf_path, min_width=100, min_height=100):
    test_name = Path(pdf_path).stem
    pdf = fitz.open(pdf_path)
    
    for question_number, img in enumerate(pdf[0].get_images()):
        if img[2] < min_width or img[3] < min_height:
            continue
        
        data = pdf.extract_image(img[0])        
        final_path = os.path.join(f"{settings.TMP_DIR}", f"{test_name}_{question_number}.webp")
        open(final_path, "wb").write(data["image"])
        
    return True