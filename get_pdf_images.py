import fitz

def extrair_imagens(pdf_path, min_largura=100, min_altura=100):
    pdf = fitz.open(pdf_path)
    for i, page in enumerate(pdf):
        for j, img in enumerate(page.get_images()):
            # img[2] = largura, img[3] = altura
            if img[2] < min_largura or img[3] < min_altura:
                continue
            
            dados = pdf.extract_image(img[0])
            open(f"img_{i}_{j}.{dados['ext']}", "wb").write(dados["image"])

extrair_imagens(r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\questoes_pdfs\questão_01.pdf")