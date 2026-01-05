import fitz

def normalizar_texto(texto):
    return ' '.join(texto.split())

def detectar_linhas_horizontais(page, espessura_max=5, margem_topo=50, margem_rodape=50, debug=False):
    """Detecta linhas horizontais no PDF e retorna suas posições Y
    
    Ignora linhas muito próximas do topo ou rodapé (geralmente são bordas do documento)
    """
    linhas_y = []
    
    drawings = page.get_drawings()
    
    if debug:
        print(f"Total de drawings encontrados: {len(drawings)}")
    
    for i, drawing in enumerate(drawings):
        rect = drawing.get("rect")
        items = drawing.get("items", [])
        
        if debug:
            print(f"  Drawing {i}: rect={rect}, items={len(items)}")
        
        # Método 1: Verifica o bounding box do drawing inteiro
        if rect:
            altura = rect.height
            largura = rect.width
            
            # Ignora linhas muito próximas do topo ou rodapé
            if rect.y0 < page.rect.y0 + margem_topo:
                if debug:
                    print(f"    → Ignorada (muito próxima do topo)")
                continue
            if rect.y1 > page.rect.y1 - margem_rodape:
                if debug:
                    print(f"    → Ignorada (muito próxima do rodapé)")
                continue
            
            # Se for largo e fino, provavelmente é uma linha
            if altura < espessura_max and largura > page.rect.width * 0.3:
                if debug:
                    print(f"    → Linha detectada via rect: y={rect.y0:.1f} a {rect.y1:.1f}")
                linhas_y.append((rect.y0 - 2, rect.y1 + 2))
                continue
        
        # Método 2: Verifica itens individuais
        for item in items:
            if item[0] == "l":  # Linha
                p1, p2 = item[1], item[2]
                
                # Ignora linhas muito próximas do topo ou rodapé
                if min(p1.y, p2.y) < page.rect.y0 + margem_topo:
                    continue
                if max(p1.y, p2.y) > page.rect.y1 - margem_rodape:
                    continue
                
                if abs(p1.y - p2.y) < espessura_max:
                    if abs(p2.x - p1.x) > page.rect.width * 0.3:
                        if debug:
                            print(f"    → Linha detectada via 'l': y={p1.y:.1f}")
                        linhas_y.append((min(p1.y, p2.y) - 2, max(p1.y, p2.y) + 2))
            
            elif item[0] == "re":  # Retângulo
                r = item[1]
                
                # Ignora linhas muito próximas do topo ou rodapé
                if r.y0 < page.rect.y0 + margem_topo:
                    continue
                if r.y1 > page.rect.y1 - margem_rodape:
                    continue
                
                if r.height < espessura_max and r.width > page.rect.width * 0.3:
                    if debug:
                        print(f"    → Linha detectada via 're': y={r.y0:.1f} a {r.y1:.1f}")
                    linhas_y.append((r.y0 - 1, r.y1 + 1))
    
    # Remove duplicatas e ordena
    linhas_y = list(set(linhas_y))
    linhas_y.sort()
    
    return linhas_y

def processar_pdf_completo(pdf_entrada, imagem_saida, pdf_saida, textos_para_remover, 
                           dpi=300, margem_inferior=0, margem_superior=0, 
                           remover_linhas=True, altura_minima_regiao=20, debug=False):
    doc = fitz.open(pdf_entrada)
    page = doc[0]
    page_rect = page.rect
    text_dict = page.get_text("dict")
    
    regioes_remover = []
    
    # Detecta linhas horizontais (ignorando topo e rodapé)
    if remover_linhas:
        linhas = detectar_linhas_horizontais(page, margem_topo=50, margem_rodape=50, debug=debug)
        regioes_remover.extend(linhas)
        print(f"✓ Linhas horizontais detectadas: {len(linhas)}")
        for l in linhas:
            print(f"    Y: {l[0]:.1f} → {l[1]:.1f}")
    
    # Margens
    if margem_superior > 0:
        regioes_remover.append((page_rect.y0, page_rect.y0 + margem_superior))
    
    if margem_inferior > 0:
        regioes_remover.append((page_rect.y1 - margem_inferior, page_rect.y1))
    
    for texto_original in textos_para_remover:
        texto_normalizado = normalizar_texto(texto_original)
        palavras = texto_normalizado.split()
        
        if len(palavras) == 0:
            continue
            
        if len(palavras) <= 3:
            texto_inicio = palavras[0]
            texto_fim = palavras[-1]
        elif len(palavras) <= 6:
            texto_inicio = " ".join(palavras[:2])
            texto_fim = " ".join(palavras[-2:])
        else:
            texto_inicio = " ".join(palavras[:3])
            texto_fim = " ".join(palavras[-3:])
        
        y_inicio = None
        y_fim = None
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    texto_linha = "".join(span["text"] for span in line["spans"])
                    texto_linha_normalizado = normalizar_texto(texto_linha)
                    
                    if texto_inicio.lower() in texto_linha_normalizado.lower() and y_inicio is None:
                        y_inicio = line["bbox"][1]
                    
                    if texto_fim.lower() in texto_linha_normalizado.lower():
                        y_fim = line["bbox"][3]
        
        if y_inicio and y_fim and y_fim > y_inicio:
            regioes_remover.append((y_inicio, y_fim))
    
    if not regioes_remover:
        regioes_manter = [(page_rect.y0, page_rect.y1)]
    else:
        regioes_remover.sort()
        
        regioes_mescladas = []
        for y_inicio, y_fim in regioes_remover:
            if regioes_mescladas and y_inicio <= regioes_mescladas[-1][1]:
                regioes_mescladas[-1] = (regioes_mescladas[-1][0], max(regioes_mescladas[-1][1], y_fim))
            else:
                regioes_mescladas.append((y_inicio, y_fim))
        
        regioes_manter = []
        y_atual = page_rect.y0
        
        for y_inicio, y_fim in regioes_mescladas:
            if y_atual < y_inicio - 1:
                regioes_manter.append((y_atual, y_inicio))
            y_atual = y_fim
        
        if y_atual < page_rect.y1 - 1:
            regioes_manter.append((y_atual, page_rect.y1))
        
        # 👇 FILTRO IMPORTANTE: Remove regiões muito pequenas
        regioes_manter = [(y_i, y_f) for y_i, y_f in regioes_manter if (y_f - y_i) >= altura_minima_regiao]
    
    if not regioes_manter:
        print("⚠ Nenhuma região válida para manter!")
        doc.close()
        return False
    
    print(f"✓ Regiões a manter (altura mínima {altura_minima_regiao}px): {len(regioes_manter)}")
    for r in regioes_manter:
        print(f"    Y: {r[0]:.1f} → {r[1]:.1f} (altura: {r[1]-r[0]:.1f})")
    
    altura_nova = sum(y_fim - y_inicio for y_inicio, y_fim in regioes_manter)
    
    novo_doc = fitz.open()
    nova_pagina = novo_doc.new_page(width=page_rect.width, height=altura_nova)
    
    y_destino = 0
    for y_inicio, y_fim in regioes_manter:
        rect_fonte = fitz.Rect(page_rect.x0, y_inicio, page_rect.x1, y_fim)
        altura_regiao = y_fim - y_inicio
        rect_destino = fitz.Rect(0, y_destino, page_rect.width, y_destino + altura_regiao)
        
        # Validação extra antes de chamar show_pdf_page
        if rect_fonte.is_empty or not rect_fonte.is_valid:
            print(f"⚠ Pulando região inválida: {rect_fonte}")
            continue
        
        nova_pagina.show_pdf_page(rect_destino, doc, 0, clip=rect_fonte)
        y_destino += altura_regiao
    
    novo_doc.save(pdf_saida)
    
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = nova_pagina.get_pixmap(matrix=mat)
    pix.save(imagem_saida)
    
    doc.close()
    novo_doc.close()
    
    print(f"✓ PDF salvo: {pdf_saida}")
    print(f"✓ Imagem salva: {imagem_saida}")
    
    return True


if __name__ == "__main__":
    pdf_path = r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\questoes_pdfs\questão_28.pdf"
    imagem_saida = r"C:\Users\thica\OneDrive\Documentos\questao_28_limpo.png"
    pdf_saida = r"C:\Users\thica\OneDrive\Documentos\questao_28_limpo.pdf"
    
    textos_para_remover = [
        """
        26
        Agronomia
        """,
        """
        *r01202327*
        VALIDINEP2023VALIDINEP2023VALIDIN3P2023VALIDINEP2023VALIDINEP2VALIDINEP
        """
    ]
    
    processar_pdf_completo(
        pdf_entrada=pdf_path,
        imagem_saida=imagem_saida,
        pdf_saida=pdf_saida,
        textos_para_remover=textos_para_remover,
        dpi=300,
        remover_linhas=True,
        # margem_inferior=10,
        altura_minima_regiao=20,  # 👈 Ignora regiões menores que 20 pontos
        debug=False
    )