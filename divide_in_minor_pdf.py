import fitz  # PyMuPDF
import re
import os

# =====================================================
# CONFIGURAÇÕES
# =====================================================

PDF_PATH = r"C:\Users\thica\OneDrive\Documentos\01 - Pessoal\001 - Dev\Projetos\lumo\lumo-etl\data\tmp\2023_PV_agronomia.pdf"
OUTPUT_DIR = "questoes_pdfs"
DPI = 250  # Usado para qualidade da renderização interna

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# REGEX
# =====================================================

QUESTAO_REGEX = re.compile(r"QUESTÃO\s+\d+", re.IGNORECASE)
ALTERNATIVA_E_REGEX = re.compile(r"^\s*[Ⓔ⊙●]?\s*E[\s\)]", re.MULTILINE)

DISCURSIVA_REGEX = re.compile(
    r"(elabore|redija|discorra|texto dissertativo|resposta discursiva|padrão de resposta)",
    re.IGNORECASE
)

PERCEPCAO_REGEX = re.compile(
    r"questionário\s+de\s+percepção",
    re.IGNORECASE
)

# =====================================================
# PROCESSAMENTO
# =====================================================

doc = fitz.open(PDF_PATH)

print("🔍 Detectando questões e alternativas...")

# Detectar todas as questões
questoes = []

for page_index, page in enumerate(doc):
    blocks = page.get_text("blocks")
    
    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        
        match_questao = QUESTAO_REGEX.search(text)
        if match_questao:
            questoes.append({
                "page": page_index,
                "y_start": y0,
                "label": match_questao.group(),
                "y_end": None,
                "page_end": None
            })

print(f"  ✓ Encontradas {len(questoes)} questões")

# Para cada questão, encontrar a alternativa E e seu FIM (último ponto final)
for i, questao in enumerate(questoes):
    encontrou_e = False
    texto_questao = ""
    
    for page_index in range(questao["page"], len(doc)):
        page = doc[page_index]
        page_text = page.get_text()
        
        if PERCEPCAO_REGEX.search(page_text):
            questao["skip"] = True
            questao["skip_reason"] = "percepcao"
            for j in range(i, len(questoes)):
                questoes[j]["skip"] = True
                questoes[j]["skip_reason"] = "percepcao"
            break
        
        if page_index <= questao["page"] + 2:
            texto_questao += page_text
        
        blocks = page.get_text("blocks")
        
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            
            if page_index == questao["page"] and y0 < questao["y_start"]:
                continue
            
            # Se já encontrou alternativa E, procurar o fim (bloco que termina com ponto)
            if encontrou_e:
                # Se encontrou próxima questão, parar (usa o y_end anterior)
                if QUESTAO_REGEX.search(text):
                    break
                
                # Atualizar y_end para este bloco
                questao["page_end"] = page_index
                questao["y_end"] = y1
                
                # Se o bloco termina com ponto final, é o fim da alternativa E
                texto_limpo = text.strip()
                if texto_limpo.endswith('.'):
                    break
            
            # Procurar alternativa E
            elif ALTERNATIVA_E_REGEX.search(text):
                encontrou_e = True
                questao["page_end"] = page_index
                questao["y_end"] = y1
                
                # Se já termina com ponto, é o fim
                texto_limpo = text.strip()
                if texto_limpo.endswith('.'):
                    break
        
        # Se já achou o fim, sair do loop de páginas
        if encontrou_e and questao["y_end"] is not None:
            texto_bloco = text.strip() if 'text' in dir() else ""
            if texto_bloco.endswith('.') or QUESTAO_REGEX.search(texto_bloco):
                break
        
        if page_index > questao["page"] + 3:
            break
    
    # Verificar se é discursiva
    if not questao.get("skip", False):
        if DISCURSIVA_REGEX.search(texto_questao):
            questao["skip"] = True
            questao["skip_reason"] = "discursiva"
            print(f"  ⊗ {questao['label']}: Discursiva (ignorada)")
        elif encontrou_e:
            print(f"  ✓ {questao['label']}: E encontrada na página {questao['page_end'] + 1}")
        else:
            print(f"  ⚠ {questao['label']}: Alternativa E não encontrada")
            questao["skip"] = True
            questao["skip_reason"] = "sem_alternativa_e"

# =====================================================
# EXTRAIR E SALVAR COMO PDF
# =====================================================

print("\n✂️ Extraindo questões como PDF...")


def extrair_questao_para_pdf(doc_origem, questao, output_path):
    """
    Extrai uma questão do PDF original e salva como novo PDF.
    """
    # Criar novo documento PDF
    novo_doc = fitz.open()
    
    pagina_inicio = questao["page"]
    pagina_fim = questao["page_end"]
    y_start = questao["y_start"]
    y_end = questao["y_end"]
    
    if pagina_inicio == pagina_fim:
        # Questão está em uma única página
        page_origem = doc_origem[pagina_inicio]
        
        # Definir área de recorte
        clip = fitz.Rect(
            0,
            y_start,
            page_origem.rect.width,
            y_end
        )
        
        # Criar nova página com tamanho do recorte
        altura_recorte = y_end - y_start
        nova_pagina = novo_doc.new_page(
            width=page_origem.rect.width,
            height=altura_recorte
        )
        
        # Copiar conteúdo da área recortada
        nova_pagina.show_pdf_page(
            nova_pagina.rect,  # Destino: página inteira
            doc_origem,
            pagina_inicio,
            clip=clip  # Origem: área recortada
        )
    else:
        # Questão atravessa múltiplas páginas
        fragmentos = []
        
        # Primeira página (do y_start até o fim)
        page_origem = doc_origem[pagina_inicio]
        clip_primeira = fitz.Rect(
            0,
            y_start,
            page_origem.rect.width,
            page_origem.rect.height
        )
        fragmentos.append({
            "page_index": pagina_inicio,
            "clip": clip_primeira,
            "altura": page_origem.rect.height - y_start
        })
        
        # Páginas intermediárias (página inteira)
        for p in range(pagina_inicio + 1, pagina_fim):
            page_inter = doc_origem[p]
            clip_inter = fitz.Rect(
                0, 0,
                page_inter.rect.width,
                page_inter.rect.height
            )
            fragmentos.append({
                "page_index": p,
                "clip": clip_inter,
                "altura": page_inter.rect.height
            })
        
        # Última página (do topo até y_end)
        page_origem = doc_origem[pagina_fim]
        clip_ultima = fitz.Rect(
            0,
            0,
            page_origem.rect.width,
            y_end
        )
        fragmentos.append({
            "page_index": pagina_fim,
            "clip": clip_ultima,
            "altura": y_end
        })
        
        # Calcular altura total e largura máxima
        altura_total = sum(f["altura"] for f in fragmentos)
        largura = doc_origem[pagina_inicio].rect.width
        
        # Criar página única com toda a questão
        nova_pagina = novo_doc.new_page(
            width=largura,
            height=altura_total
        )
        
        # Posicionar cada fragmento
        y_offset = 0
        for fragmento in fragmentos:
            destino = fitz.Rect(
                0,
                y_offset,
                largura,
                y_offset + fragmento["altura"]
            )
            
            nova_pagina.show_pdf_page(
                destino,
                doc_origem,
                fragmento["page_index"],
                clip=fragmento["clip"]
            )
            
            y_offset += fragmento["altura"]
    
    # Salvar PDF
    novo_doc.save(output_path, garbage=4, deflate=True)
    novo_doc.close()


# Processar cada questão
for questao in questoes:
    if questao.get("skip", False):
        reason = questao.get("skip_reason", "desconhecido")
        if reason == "discursiva":
            print(f"  ⊗ Pulando {questao['label']} (discursiva)")
        elif reason == "percepcao":
            print(f"  ⊗ Pulando {questao['label']} (questionário de percepção)")
        elif reason == "sem_alternativa_e":
            print(f"  ⊗ Pulando {questao['label']} (sem alternativa E)")
        continue
    
    if questao["y_end"] is None:
        print(f"  ⊗ Pulando {questao['label']} (sem alternativa E)")
        continue
    
    # Gerar nome do arquivo
    nome = questao["label"].replace(" ", "_").lower()
    output_path = os.path.join(OUTPUT_DIR, f"{nome}.pdf")
    
    # Extrair e salvar
    extrair_questao_para_pdf(doc, questao, output_path)
    
    print(f"  ✓ Salvo: {nome}.pdf")

doc.close()

print("\n✅ Processamento concluído!")
print(f"📁 PDFs salvos em: {OUTPUT_DIR}")