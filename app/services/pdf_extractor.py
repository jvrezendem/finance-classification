#extrai os dados do pdf

from dataclasses import dataclass
from pathlib import Path
import pymupdf

@dataclass
class Pagina:
    page_num: int 
    text: str
    extraction_method: str

class PDFExtractionError(Exception):
    pass


def precisa_ocr(text:str):
    conteudo = text.strip()

    if not conteudo:
        return True

    num_caracteres = 0
    for c in conteudo:
        if c.isalnum():
            num_caracteres +=1

    #se o numero de caracteres validos for menor que 20, precisa de ocr
    return num_caracteres < 20

#extrair conteudo do pdf
def extrair_paginas_pdf(caminho_pdf:Path):
    if not caminho_pdf.exists():
        raise FileNotFoundError(f"PDF não econtrado em {caminho_pdf}")

    try:
        doc = pymupdf.open(caminho_pdf)
    except Exception as e:
        raise IOError(f"Erro ao abrir pdf {caminho_pdf}: {e}")

    pages:list[Pagina] = []

    try:
        for i, page in enumerate(doc):
            pg_num = i+1
            texto = page.get_text("text") 
            
            if precisa_ocr(texto):
                try:
                    text_page = page.get_textpage_ocr(language="por", dpi=300, full=True)
                        
                    page_text = page.get_text(
                        "text",
                        textpage=text_page
                    )

                    method = "ocr"
                except Exception as e:
                    raise PDFExtractionError(
                        f"Falha no OCR da pagina {pg_num}: {str(e)}"
                    )
            else:
                page_text = texto
                method = "digital"

            pages.append(
                Pagina(
                    page_num=pg_num,
                    text=page_text.strip(),
                    extraction_method=method
                )
            )
    finally:    
        doc.close()
        
    return pages